import pandas as pd

default_user = {"F": 0, "M": 1, "Age": "22", "Occupation": 1, "Action": 0.26292, "Adventure": 0.136199, "Animation": 0.045813, "Family": 0.06975, "Comedy": 0.348596, "Crime": 0.090367, "Documentary": 0.007849, "Drama": 0.365773, "Fantasy": 0.036633, "Film-Noir": 0.0222595, "Horror": 0.071675, "Music": 0.039808, "Mystery": 0.041178, "Romance": 0.147283, "Science Fiction": 0.16773, "Thriller": 0.195006, "War": 0.07857, "Western": 0.019571}

all_categories = ['Action', 'Adventure', 'Animation', "Family", 'Comedy', 'Crime', 'Documentary',
              'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Music', 'Mystery', 'Romance',
              'Science Fiction', 'Thriller', 'War', 'Western']

def predict_rating_for_user(rating_regressor, categories, user):
    cat_features = {cat: 1 if cat in categories else 0 for cat in all_categories}
    user = {col + '_user_pref' if col in all_categories else col: val for col, val in user.items()} 
    input_data = {**cat_features, **user}
    input_df = pd.DataFrame([input_data], index=[0])
    return rating_regressor.predict(input_df)[0]