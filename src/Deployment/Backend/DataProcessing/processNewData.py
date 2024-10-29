import pandas as pd

from API.getMeteorological import get_daily_meteorological
from API.getPollutans import get_daily_pollutans
from dataProcessingUtil import (
    load_data_information,
    handle_missing_data,
    clip_outliers,
    scale_datapoint,
    remove_features,
    cap_min_max,
    add_datapoint,
    create_datetime_features,
    create_seasonal_features,
)


def new_datapoint_processing_pipeline():
    # Get daily pollutans DF
    pollutans_df = get_daily_pollutans()
    pollutans_df.index = pd.to_datetime(pollutans_df.index).strftime("%Y-%m-%d")

    # Get daily meteorological DF
    meteorological_df = get_daily_meteorological()
    meteorological_df.index = pd.to_datetime(meteorological_df.index).strftime(
        "%Y-%m-%d"
    )

    # Concatenate and produce the new datapoint
    new_datapoint = pd.concat([pollutans_df, meteorological_df], axis=1)
    new_datapoint.index = pd.to_datetime(new_datapoint.index)

    # Load feature information for datapoint preprocessing.
    feature_info = load_data_information()
    features = feature_info.get("features", [])
    min_max_values = feature_info.get("min_max", {})
    mean_std_values = feature_info.get("mean_std", {})

    new_datapoint = remove_features(new_datapoint, features)
    new_datapoint = handle_missing_data(new_datapoint, mean_std_values, features)
    new_datapoint = clip_outliers(new_datapoint, mean_std_values, features)
    cap_min_max(new_datapoint)
    new_datapoint = scale_datapoint(new_datapoint, min_max_values, features)

    new_datapoint = create_datetime_features(new_datapoint)
    new_datapoint = create_seasonal_features(new_datapoint)

    add_datapoint(new_datapoint)


new_datapoint_processing_pipeline()
