import pandas as pd

from API.getMeteorologicalDaily import get_daily_meteorological
from API.getTargetDaily import get_daily_targets
from Utils.dataPointPreprocessingUtil import (
    load_json_file,
    remove_features,
    clip_outliers,
    scale_datapoint,
    handle_missing_data,
)

from Utils.dataPreprocessingUtil import (
    create_seasonal_features,
    create_datetime_features,
)

from DataBase.addDatapoint import add_datapoint


def stream_new_datapoint():
    target_df = get_daily_targets()
    target_df.index = pd.to_datetime(target_df.index).strftime("%Y-%m-%d")

    meteorological_df = get_daily_meteorological()
    meteorological_df.index = pd.to_datetime(meteorological_df.index).strftime(
        "%Y-%m-%d"
    )

    new_datapoint = pd.concat([target_df, meteorological_df], axis=1)
    new_datapoint.index = pd.to_datetime(new_datapoint.index)

    feature_info = load_json_file()
    features = feature_info.get("features", [])
    min_max_values = feature_info.get("min_max", {})
    mean_std_values = feature_info.get("mean_std", {})

    new_datapoint = remove_features(new_datapoint, features)
    new_datapoint = handle_missing_data(new_datapoint, mean_std_values, features)
    new_datapoint = clip_outliers(new_datapoint, mean_std_values, features)
    new_datapoint = scale_datapoint(new_datapoint, min_max_values, features)

    new_datapoint = create_datetime_features(new_datapoint)
    new_datapoint = create_seasonal_features(new_datapoint)

    add_datapoint(new_datapoint)


stream_new_datapoint()
