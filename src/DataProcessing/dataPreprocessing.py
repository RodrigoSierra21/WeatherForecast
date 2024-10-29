import pandas as pd
import numpy as np

from Utils.dataPreprocessingUtil import (
    smooth_outliers,
    create_datetime_features,
    create_seasonal_features,
    scale_data,
    missing_percentages,
    get_mean_values,
    get_min_max_values,
    store_values,
)

from Utils.dataPreprocessingPlots import (
    boxplot_monthly_variation_no2,
    boxplot_monthly_variation_o3,
    boxplot_yearly_variation,
    boxplot_weekly_variation_no2,
    boxplot_weekly_variation_o3,
    plot_histograms,
)

# Open the csv file
df = pd.read_csv("./Datasets/Raw/Targets.csv", index_col=0)

# Set the index to datetime
df.index = pd.to_datetime(df.index, errors="coerce")
df.replace(r"^\s*$|[^0-9.]+", np.nan, regex=True, inplace=True)

# Interpolate missin values
df = df.apply(pd.to_numeric, errors="coerce")
df = df.interpolate(method="linear").interpolate(method="nearest")

# Same for the weather df
weatherdf = pd.read_csv("./Datasets/Raw/MeteorologicalFeatures.csv", index_col=0)

# missing percentages(weatherdf)
# plot_correlation_matrix(weatherdf)

# Drop ccollumns with a high correlation or too many missing values
weatherdf = weatherdf.drop(columns=["wpgt", "tsun", "tmax", "tmin", "snow"])

# Make the index column the same for easier concatenation
df = df[df.index >= "2018-01-01"]
df = df.reset_index()
df.rename(columns={"index": "DateTime"}, inplace=True)

weatherdf = weatherdf.reset_index()
weatherdf.rename(columns={"index": "time"}, inplace=True)

# Concatenate the dataframes
df = pd.concat([df, weatherdf], axis=1)
df = df.drop(columns=["time"])
df = df.set_index("DateTime")

# Remove outliers
df = smooth_outliers(df)


# Store the dataset information (mean-stds/min-max/feature names)
numeric_features = df.select_dtypes(include=["number"])
min_max = get_min_max_values(numeric_features)
mean_std = get_mean_values(numeric_features)
# Uncomment tooverwrite the current file
# store_values(min_max, mean_std, numeric_features)

# plot_correlation_matrix(df)

df = scale_data(df)
df = create_datetime_features(df)
df = create_seasonal_features(df)

# boxplot_monthly_variation_o3(df)
# boxplot_weekly_variation_o3(df)

# boxplot_monthly_variation_no2(df)
# boxplot_weekly_variation_no2(df)

# boxplot_yearly_variation(df)
# plot_histograms(df)

# print(missing_percentages(df))

# df.to_csv("./Datasets/Processed/preprocessed_data.csv", index=False)
