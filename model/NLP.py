import numpy
import pandas
import fasttext
import csv
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.layers import Dense, InputLayer, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
from math import floor
from random import random
from functools import reduce
from Vectorizer import Tokenize, Load_Vectorizer

Genres = [
    "Comedy",
    "Drama",
    "Romance",
    "Action",
    "Crime",
    "Thriller",
    "Adventure",
    "Family",
    "Animation",
    "Horror",
    "Mystery",
    "Science Fiction",
    "Fantasy",
    "War",
    "Western",
    "Music",
    "History",
    "Foreign",
    "Documentary",
    "TV Movie",
]


def Encode_Genre(List):
    Output = []
    for Genre in Genres:
        if Genre in List:
            Output.append(1)
        else:
            Output.append(0)
    return Output


def Decode_Genre(List):
    Output = []
    for Index in range(len(List)):
        if List[Index] > 0.5:
            Output.append(Genres[Index])
    return Output


def Process_Point(Point, Vectorizer, Padding=40):
    Input = list(map(lambda X: Vectorizer[X], Tokenize(Point[0])))[0:Padding]
    for _ in range(Padding - len(Input)):
        Input.append([0 for _ in range(100)])
    return [
        list(map(lambda X: list(map(lambda Y: float(Y), X)), Input)),
        Encode_Genre(Point[1]),
    ]


def Train_Model(
    X, Y, Epochs=100, Learning_Rate=0.001, Previous_Model=None, Name="Model"
):
    Model = Previous_Model
    if Model == None:
        Model = Sequential()
        Model.add(InputLayer((10, 100)))
        Model.add(LSTM(128))
        Model.add(Dense(16, "relu"))
        Model.add(Dense(len(Genres), "linear"))
        Model.compile(
            loss=MeanSquaredError(),
            optimizer=Adam(learning_rate=Learning_Rate),
            metrics=[RootMeanSquaredError()],
        )
    Model.fit(
        numpy.array(X),
        numpy.array(Y),
        epochs=Epochs,
        callbacks=[
            ModelCheckpoint(Name + ".keras", save_best_only=True, monitor="loss")
        ],
    )
    Model.save(Name + ".keras")
    return Model


def Predict(Batch, Model, Vectorizer):
    return Model.predict(
        numpy.array(
            list(map(lambda Point: Process_Point([Point, []], Vectorizer)[0], Batch))
        )
    )


def Measure(Batch, Model, Vectorizer):
    Points = list(map(lambda Point: Process_Point(Point, Vectorizer), Batch))
    Targets = list(map(lambda Point: Point[1], Points))
    Outputs = list(
        Model.predict(numpy.array(list(map(lambda Point: Point[0], Points))))
    )
    TP = 0
    FN = 0
    FP = 0
    for I in range(len(Targets)):
        for J in range(len(Genres)):
            if round(Outputs[I][J]) == round(Targets[I][J]):
                TP += round(Outputs[I][J])
            else:
                FN += 1 - round(Outputs[I][J])
                FP += round(Outputs[I][J])
    Recall = TP / (TP + FN)
    Precision = TP / (TP + FP)
    return [Recall, Precision, 2 * Precision * Recall / (Precision + Recall)]
