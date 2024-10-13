from API.getDailyData import get_datapoint
import sqlite3

df = get_datapoint()

db_path = "./Data/DataBase/pollutionDataBase.db"
conn = sqlite3.connect(db_path)

table_name = "Air_Pollution_Data"

df.to_sql(table_name, conn, if_exists="append", index=False)


conn.commit()
conn.close()
