import json


def load_json_file():
    with open("./Datasets/FeatureInformation/dataset_information.json", "r") as file:
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


def scale_datapoint(df, min_max_values, features):
    for feature in features:
        min = min_max_values[feature]["min"]
        max = min_max_values[feature]["max"]

        df[feature] = (df[feature] - min) / (max - min)

    return df
