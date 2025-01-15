import fasttext
import csv
import json


def Tokenize(Sentence):
    return (
        Sentence.lower()
        .replace(".", " .")
        .replace(",", " ,")
        .replace("!", " !")
        .replace("?", " ?")
        .replace(":", " :")
        .replace(";", " ;")
        .replace("'", " ' ")
        .replace('"', ' " ')
        .replace("   ", " ")
        .replace("  ", " ")
        .split(" ")
    )


def Train(File):
    Model = fasttext.train_unsupervised(File, model="skipgram")
    Model.save_model("Model.ftz")
    return Model


def Load_Vectorizer(File):
    return fasttext.load_model(File)
