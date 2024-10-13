import pandas as pd
import sqlite3

df = pd.read_csv("./Data/Datasets/raw/daily_data.csv")

conn = sqlite3.connect("./Data/DataBase/pollutionDataBase.db")

table_name = "Air Pollution Data"  
df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.commit()
conn.close()

