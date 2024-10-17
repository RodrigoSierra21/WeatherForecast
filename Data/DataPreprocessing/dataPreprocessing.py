import pandas as pd
import numpy as np

from dataPreprocessingUtil import (
    smooth_outliers,
    create_datetime_features,
    create_seasonal_features,
    scale_data,
    missing_percentages,
)

from dataPreprocessingPlots import (
    boxplot_monthly_variation_no2,
    boxplot_monthly_variation_o3,
    boxplot_yearly_variation,
    boxplot_weekly_variation_no2,
    boxplot_weekly_variation_o3,
)

df = pd.read_csv("./Data/Datasets/raw/dataset.csv")
df = df.drop(columns=["Unnamed: 0"])
df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")
df.set_index("DateTime", inplace=True)

# Replace any empy value with nan
df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

# Interpolate missing values using linear, followed by nearest method for any remaining NaNs.
df = df.apply(pd.to_numeric, errors="coerce")
df = df.interpolate(method="linear").interpolate(method="nearest")
df = df.resample("D").mean().round(4)

weatherdf = pd.read_csv("./Data/Datasets/raw/weather_data.csv")
weatherdf["date"] = pd.to_datetime(weatherdf["date"]).dt.normalize()
weatherdf.set_index("date", inplace=True)

# missing percentages(weatherdf)
weatherdf = weatherdf.drop(columns=["wpgt", "tsun", "tmax", "tmin"])
weatherdf = weatherdf[weatherdf.index.isin(df.index)]
df = pd.merge(df, weatherdf, left_index=True, right_index=True)


# Check if there are any missing dates
full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
df = df.reindex(full_date_range)


# Replace any empy value with nan
df.replace(r"^\s*$", np.nan, regex=True, inplace=True)

# Interpolate missing values using linear, followed by nearest method for any remaining NaNs.
df = df.apply(pd.to_numeric, errors="coerce")
df = df.interpolate(method="linear").interpolate(method="nearest")


df = smooth_outliers(df)


# plot_correlation_matrix(df)

df = scale_data(df)


df = create_datetime_features(df)
# df = create_seasonal_features(df)


# boxplot_monthly_variation_o3(df)
# boxplot_weekly_variation_o3(df)

# boxplot_monthly_variation_no2(df)
# boxplot_weekly_variation_no2(df)

# boxplot_yearly_variation(df)

# print(missing_percentages(df))
# print(df)

# df.to_csv("./Data/Datasets/Processed/preprocessed_data_all.csv", index=False)
