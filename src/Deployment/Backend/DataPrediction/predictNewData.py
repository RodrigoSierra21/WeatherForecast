import numpy as np

from DataPrediction.performanceMonitoring import add_metrics_data
from DataPrediction.predictUtils import (
    load_features,
    get_rows,
    descale_datapoint,
    load_json_file,
    load_champion_model,
)


def predict_data(target_column):

    # Retrieve the last five days
    last_datapoint = get_rows(5)

    # Get the last day before predictions
    last_day = last_datapoint["DateTime"].iloc[0]

    # De scale predictions
    feature_info = load_json_file()
    min_max_values = feature_info.get("min_max", {})

    # Select features for O3
    features = load_features(target_column)
    df = last_datapoint[features]

    # Load model for O3
    model = load_champion_model(
        f"./src/Deployment/Data/ChampionModels/model{target_column}.pkl"
    )

    datapoint = df.to_numpy().reshape(5, len(features))
    datapoint = datapoint.flatten()
    datapoint = datapoint.reshape(1, 5 * len(features))
    pred = model.predict(datapoint)
    predictions = descale_datapoint(pred, min_max_values, target_column)
    last_target_values = last_datapoint[target_column].values
    last_target_values = descale_datapoint(
        last_target_values, min_max_values, target_column
    )
    last_target_values = last_target_values.values
    last_target_values = last_target_values.flatten()

    # Get the first three predictions
    predictions = predictions.values
    predictions = predictions.flatten()

    # Add predictions to performance monitoring database
    add_metrics_data(last_day, predictions, target_column)

    values = np.concatenate([last_target_values, predictions])

    return values
