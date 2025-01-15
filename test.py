import NLP

Model = NLP.load_model("Model.keras")

print(
    NLP.Decode_Genre(
        NLP.Predict(
            [
                "Angela Basset was good as expected, but Whitney has no Range as an actress. The screenplay also neglected to portray, on film, the greatness of this novel.  Instead of promoting sisterhood, they emphasized the canine-qualities of men.  Read the book; rent Soul Food instead!"
            ],
            Model,
            NLP.Load_Vectorizer("Model.ftz"),
        )[0]
    )
)