import pandas as pd
from sklearn.linear_model import LinearRegression
#from scrape import data_scrape as ds
import get_data as get_data
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

def create_model():
    #---------------------------------------------------------
    #Selecting Data
    #---------------------------------------------------------

    df = get_data.get_mongo_data()

    #---------------------------------------------------------
    #Cleaning Data
    #---------------------------------------------------------

    df['episodes'] = df['episodes'].replace('?', pd.NA)

    df['episodes'] = pd.to_numeric(df['episodes'], errors='coerce')

    df = df.dropna(subset=['episodes', 'timespans'])
    df = df[df['timespans'] != 0]

    df.reset_index(drop=True, inplace=True)

    #---------------------------------------------------------
    #Linear Regression
    #---------------------------------------------------------

    df_shuffled = df.sample(frac=1, random_state=42)

    X = df_shuffled[['episodes', 'members', 'timespans']]
    y = df_shuffled['ratings']

    model = LinearRegression()

    model.fit(X, y)

    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)

    r_squared_before = model.score(X, y)
    print("R-squared before removing outliers:", r_squared_before)

    residuals = np.abs(model.predict(X) - y)

    #!!More threshold tests required!!
    threshold = 0.8 * np.std(residuals)

    filtered_df = df_shuffled[residuals <= threshold]

    global X_filtered
    global y_filtered
    X_filtered = filtered_df[['episodes', 'members', 'timespans']]
    y_filtered = filtered_df['ratings']

    model.fit(X_filtered, y_filtered)

    print("Coefficients after removing outliers:", model.coef_)
    print("Intercept after removing outliers:", model.intercept_)

    r_squared_after = model.score(X_filtered, y_filtered)
    print("R-squared after removing outliers:", r_squared_after)

    return model

#---------------------------------------------------------
#Plot
#---------------------------------------------------------

def plot_model(x, y):
    predicted_ratings = model.predict(x)

    plt.figure(figsize=(10, 6))
    plt.scatter(y, predicted_ratings, color='blue', label='Actual vs. Predicted Ratings')
    plt.xlabel('Actual Ratings')
    plt.ylabel('Predicted Ratings')
    plt.title('Actual vs. Predicted Ratings')
    plt.legend()
    plt.grid(True)

    min_value = min(min(y), min(predicted_ratings))
    max_value = max(max(y), max(predicted_ratings))
    plt.plot([min_value, max_value], [min_value, max_value], color='red', linestyle='--', label='Diagonal Line')

    if not os.path.exists('../web/img/plot.png'):
        plt.savefig('../web/img/plot.png')


#---------------------------------------------------------
#Predict
#---------------------------------------------------------

def model_predict(model,new_episode,new_member,new_timespan):
    to_predict = {
        'Episodes': new_episode,
        'Members': new_member,
        'Timespans': new_timespan
    }
    return model.predict(to_predict)

#---------------------------------------------------------
#Save model
#---------------------------------------------------------
model = create_model()

model_filepath = '../model/anime_model.pkl'

with open(model_filepath, 'wb') as f:
    pickle.dump(model, f)

#plot_model(X_filtered,y_filtered)
