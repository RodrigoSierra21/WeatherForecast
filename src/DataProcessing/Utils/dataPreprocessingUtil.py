import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import MinMaxScaler


def missing_percentages(df):
    # Calculate the percentage of missing values again
    total_rows = len(df)
    missing_percentage = (df.isnull().sum() / total_rows) * 100

    # Display the missing percentage for each column
    print(missing_percentage)


def smooth_outliers(df, threshold=3, window_size=30):
    # Calculate Z-scores
    z_scores = np.abs((df - df.mean()) / df.std())

    # Create a copy of the DataFrame to avoid modifying the original
    smoothed_df = df.copy()

    # Identify outliers
    outliers = z_scores > threshold

    # Smooth outliers with rolling mean
    for column in df.columns:
        # Apply smoothing only to outliers
        smoothed_df[column] = np.where(
            outliers[column],
            df[column].rolling(window=window_size, center=True, min_periods=1).mean(),
            df[column],
        )

    return smoothed_df


def create_datetime_features(df):
    # Create features based on the index
    df["year"] = df.index.year
    df["month"] = df.index.month
    df["day"] = df.index.day
    df["day_of_week"] = df.index.dayofweek
    df["week_of_year"] = df.index.isocalendar().week

    return df


def create_seasonal_features(df):
    df["is_spring"] = df["month"].apply(lambda x: 1 if 3 <= x <= 5 else 0)
    df["is_summer"] = df["month"].apply(lambda x: 1 if 6 <= x <= 8 else 0)
    df["is_autumn"] = df["month"].apply(lambda x: 1 if 9 <= x <= 11 else 0)
    df["is_winter"] = df["month"].apply(lambda x: 1 if x == 12 or x <= 2 else 0)

    return df


def scale_data(df):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    scaled_df = pd.DataFrame(scaled_data, columns=df.columns, index=df.index)
    return scaled_df


# Gets the mean and std values of all the features in the dataset
def get_mean_values(df):
    mean_std = {
        feature: {"mean": df[feature].mean(), "std": df[feature].std()}
        for feature in df.columns
    }

    return mean_std


# Gets the max and min vlaues for all the features in the dataset
def get_min_max_values(df):
    min_max = {
        feature: {"min": df[feature].min(), "max": df[feature].max()}
        for feature in df.columns
    }

    return min_max


# Puts all the gathered values in a dictionary in a json file for further use
def store_values(min_max, mean_std, features):
    values_to_store = {
        "mean_std": mean_std,
        "min_max": min_max,
        "features": list(features.columns),
    }

    with open(
        "./Datasets/FeatureInformation/dataset_information.json", "w"
    ) as json_file:
        json.dump(values_to_store, json_file, indent=4)
