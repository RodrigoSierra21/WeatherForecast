import json
import pandas as pd
import sqlite3


def load_features(target_column):
    try:
        with open(
            f"./Datasets/FeatureInformation/features{target_column}.json", "r"
        ) as file:
            features = json.load(file)  # Load the JSON data
            return features  # Return the loaded features
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []


def get_rows(num_rows):
    conn = sqlite3.connect("./Datasets/DataBases/pollutionDataBase.db")

    # Create the SQL query to fetch the last n rows
    query = f"""
        SELECT * 
        FROM "Air Pollution Data" 
        ORDER BY rowid DESC 
        LIMIT ?
    """

    # Execute the query and fetch the last n rows
    df = pd.read_sql(query, conn, params=(num_rows,))

    # Close the connection
    conn.close()

    # Return the resulting DataFrame
    return df


def scale_datapoint(arr, min_max_values, feature):

    df = pd.DataFrame(arr, columns=[feature])

    min = min_max_values[feature]["min"]
    max = min_max_values[feature]["max"]

    df[feature] = (df[feature] - min) / (max - min)

    return df


def load_json_file():
    with open("./Datasets/FeatureInformation/dataset_information.json", "r") as file:
        data = json.load(file)
    return data


def load_champion_model(model_path):
    # Load the model from the specified path
    model = None
    try:
        model = model.load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
    except Exception as e:
        print(f"Failed to load model from {model_path}: {e}")

    return model
