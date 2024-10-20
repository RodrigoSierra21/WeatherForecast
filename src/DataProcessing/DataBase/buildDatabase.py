import pandas as pd
import sqlite3

df = pd.read_csv("./Datasets/Processed/preprocessed_data.csv")
df.reset_index(inplace=True)
df.rename(columns={"index": "DateTime"}, inplace=True)

start_date = "2018-01-01"
num_days = len(df)
date_range = pd.date_range(start=start_date, periods=num_days, freq="D")
df["DateTime"] = date_range
df["DateTime"] = df["DateTime"].dt.strftime("%Y-%m-%d")


conn = sqlite3.connect("./Datasets/DataBases/pollutionDataBase.db")
df.to_sql("Air Pollution Data", conn, if_exists="replace", index=False)
conn.commit()
conn.close()
