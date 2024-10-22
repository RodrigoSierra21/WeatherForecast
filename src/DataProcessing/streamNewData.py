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

from Utils.dataDistributionShiftUtil import (
    check_equal_values,
    data_distribution_shift_t_test,
    plot_distribution_shift,
)

from DataBase.addDatapoint import add_datapoint, addDistributionShiftValue

from DataBase.getData import get_rows, get_rows_by_week_index


def stream_new_datapoint():

    # Add the new datapoint to the general database
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

    # Once the is added check for data distribution shifts

    # We check if the last seven rows have the same week_of_year value
    week_data = get_rows(
        7, "./Datasets/DataBases/pollutionDataBase.db", "Air Pollution Data"
    )

    # If the last seven days are from the same week.
    if check_equal_values(week_data):

        # Check if there is a data distribution shift
        week_of_year = week_data["week_of_year"].iloc[0]
        for feature in week_of_year.columns:
            rows = get_rows_by_week_index(week_of_year, feature)
            mean_value = week_data[feature].mean()
            if data_distribution_shift_t_test(rows, mean_value):
                print("Data Distribution shift detected¡¡¡¡¡")
                rows.append(mean_value)
                plot_distribution_shift(rows)

        # Add the new information to the database
        addDistributionShiftValue(week_data)


stream_new_datapoint()
