import sqlite3
import shutil

# Define the index above which to delete entries
delete_date = "2024-10-01"

# Define the paths for the source and target databases
source_db = "./Datasets/DataBases/pollutionDataBase.db"
target_db = "./src/Deployment/Data/Databases/pollutionData.db"

shutil.copyfile(source_db, target_db)

conn_target = sqlite3.connect(target_db)
cursor_target = conn_target.cursor()

delete_query = "DELETE FROM [Air Pollution Data] WHERE DateTime < ?"
cursor_target.execute(delete_query, (delete_date,))

# Step 4: Commit the changes and close the connection
conn_target.commit()
conn_target.close()
