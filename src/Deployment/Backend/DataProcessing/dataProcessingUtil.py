import json
import sqlite3


def load_data_information():
    with open(
        "./src/Deployment/Data/FeatureInformation/dataset_information.json", "r"
    ) as file:
        data = json.load(file)
    return data


def remove_features(df, features):
    features_to_drop = [col for col in df.columns if col not in features]
    return df.drop(columns=features_to_drop)


def handle_missing_data(df, mean_std_values, features):
    for feature in features:
        if df[feature].isnull().any():
            df[feature].fillna(mean_std_values[feature]["mean"], inplace=True)

    return df


def clip_outliers(df, mean_std_values, features):
    for feature in features:
        mean = mean_std_values[feature]["mean"]
        std = mean_std_values[feature]["std"]

        lower_bound = mean - 3 * std
        upper_bound = mean + 3 * std
        df[feature] = df[feature].clip(lower_bound, upper_bound)

    return df


def cap_min_max(new_data_point):
    # Load the JSON file
    data = load_data_information()
    features = data.get("features", [])

    # Iterate over each feature in the new data point
    for feature in features:

        new_value = new_data_point[feature].iloc[0]

        # Access current min and max for this feature
        current_min = data["min_max"][feature]["min"]
        current_max = data["min_max"][feature]["max"]

        # Update min if new_value is less than the current min
        if new_value < current_min:
            data["min_max"][feature]["min"] = new_data_point[feature]

        # Update max if new_value is greater than the current max
        if new_value > current_max:
            data["min_max"][feature]["max"] = new_data_point[feature]

    # Save the updated min_max values back to the JSON file
    with open(
        "./src/Deployment/Data/FeatureInformation/dataset_information.json", "w"
    ) as f:
        json.dump(data, f, indent=4)


def scale_datapoint(df, min_max_values, features):
    for feature in features:
        min = min_max_values[feature]["min"]
        max = min_max_values[feature]["max"]

        df[feature] = (df[feature] - min) / (max - min)

    return df


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


def add_datapoint(new_datapoint):
    conn = sqlite3.connect("./src/Deployment/Data/Databases/pollutionData.db")

    # Keep the index of the datapoint
    new_datapoint.reset_index(inplace=True)
    new_datapoint.rename(columns={"index": "DateTime"}, inplace=True)
    new_datapoint["DateTime"] = new_datapoint["DateTime"].dt.strftime("%Y-%m-%d")

    # Inset the new datapoint
    new_datapoint.to_sql("Air Pollution Data", conn, if_exists="append", index=False)

    # Commit changes
    conn.commit()

    # Close the database connection
    conn.close()
