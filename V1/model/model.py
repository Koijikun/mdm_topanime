import pandas as pd
from sklearn.linear_model import LinearRegression
from scrape import data_scrape as ds
import matplotlib.pyplot as plt
import numpy as np
import pickle

def create_model(episodes,members,timespans,ratings):
    #---------------------------------------------------------
    #Selecting Data
    #---------------------------------------------------------
    data = {
        'Episodes': episodes,
        'Members': members,
        'Timespans': timespans,
        'Ratings': ratings
    }

    df = pd.DataFrame(data)

    #---------------------------------------------------------
    #Cleaning Data
    #---------------------------------------------------------

    # Replace '?' with NaN in the 'episodes' column
    df['Episodes'] = df['Episodes'].replace('?', pd.NA)

    # Convert the 'episodes' column to numeric
    df['Episodes'] = pd.to_numeric(df['Episodes'], errors='coerce')

    # Drop rows where episodes are NaN or timespan is 0
    df = df.dropna(subset=['Episodes', 'Timespans'])
    df = df[df['Timespans'] != 0]

    # Reset index
    df.reset_index(drop=True, inplace=True)

    #---------------------------------------------------------
    #Linear Regression
    #---------------------------------------------------------

    # Shuffle the data before removing outliers
    df_shuffled = df.sample(frac=1, random_state=42)

    # Separate features (X) and target (y)
    X = df_shuffled[['Episodes', 'Members', 'Timespans']]
    y = df_shuffled['Ratings']

    # Initialize the linear regression model
    model = LinearRegression()

    # Fit the model
    model.fit(X, y)

    # Print the coefficients
    print("Coefficients:", model.coef_)
    print("Intercept:", model.intercept_)

    # Calculate R-squared before removing outliers
    r_squared_before = model.score(X, y)
    print("R-squared before removing outliers:", r_squared_before)

    # Calculate residuals
    residuals = np.abs(model.predict(X) - y)

    #!!More threshold tests required!!
    threshold = 0.8 * np.std(residuals)

    # Filter the dataframe to remove outliers
    filtered_df = df_shuffled[residuals <= threshold]

    # Separate features (X) and target (y) from the filtered dataframe
    global X_filtered
    global y_filtered
    X_filtered = filtered_df[['Episodes', 'Members', 'Timespans']]
    y_filtered = filtered_df['Ratings']

    # Fit the model with filtered data
    model.fit(X_filtered, y_filtered)

    # Print the coefficients after removing outliers
    print("Coefficients after removing outliers:", model.coef_)
    print("Intercept after removing outliers:", model.intercept_)

    # Calculate R-squared after removing outliers
    r_squared_after = model.score(X_filtered, y_filtered)
    print("R-squared after removing outliers:", r_squared_after)

    return model

#---------------------------------------------------------
#Plot
#---------------------------------------------------------

def plot_model(x,y):
    # Predict ratings using the model
    predicted_ratings = model.predict(x)

    # Plot actual ratings against predicted ratings
    plt.figure(figsize=(10, 6))
    plt.scatter(y, predicted_ratings, color='blue', label='Actual vs. Predicted Ratings')
    plt.xlabel('Actual Ratings')
    plt.ylabel('Predicted Ratings')
    plt.title('Actual vs. Predicted Ratings')
    plt.legend()
    plt.grid(True)
    plt.show()

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
model = create_model(ds.episodes, ds.members, ds.timespans, ds.ratings)

model_filepath = 'model/anime_model.pkl'

# Save the model to disk
with open(model_filepath, 'wb') as f:
    pickle.dump(model, f)

#model = create_model(ds.episodes, ds.members, ds.timespans, ds.ratings)
plot_model(X_filtered,y_filtered)