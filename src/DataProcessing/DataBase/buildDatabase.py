import pandas as pd
import sqlite3

# Builds a general database with all the training data that will be used
# to create the deployment databses

# Access the training data
df = pd.read_csv("./Datasets/Processed/preprocessed_data.csv")

# Keep the index
df.reset_index(inplace=True)
df.rename(columns={"index": "DateTime"}, inplace=True)

# Set the dataset range
start_date = "2018-01-01"
num_days = len(df)
date_range = pd.date_range(start=start_date, periods=num_days, freq="D")
df["DateTime"] = date_range
df["DateTime"] = df["DateTime"].dt.strftime("%Y-%m-%d")

# Connect with the database
conn = sqlite3.connect("./Datasets/DataBases/pollutionDataBase.db")

# Convert the data to sql format
df.to_sql("Air Pollution Data", conn, if_exists="replace", index=False)

# Commit and close the connection
conn.commit()
conn.close()
