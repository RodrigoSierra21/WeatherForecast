import pandas as pd
import numpy as np

from dataPreprocessingUtil import smooth_outliers, create_datetime_features, create_seasonal_features, scale_data

df = pd.read_csv("./Data/Datasets/raw/daily_data.csv")
df["date"] = pd.to_datetime(df["date"])
df.set_index("date", inplace=True)

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

df = create_datetime_features(df)
df = create_seasonal_features(df)
df = scale_data(df)

# print(missing_percentages(df))

df.to_csv("./Data/Datasets/Processed/preprocessed_data.csv", index=False)