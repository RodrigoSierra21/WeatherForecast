import sqlite3


def add_datapoint(new_datapoint):
    conn = sqlite3.connect("./Datasets/DataBases/pollutionDataBase.db")

    # Keep the index of the datapoint
    new_datapoint.reset_index(inplace=True)
    new_datapoint.rename(columns={"index": "DateTime"}, inplace=True)
    new_datapoint["DateTime"] = new_datapoint["DateTime"].dt.strftime("%Y-%m-%d")

    # Inset the new datapoint
    new_datapoint.to_sql("Air Pollution Data", conn, if_exists="append", index=False)

    # Commit changes
    conn.commit()

    # Close the database connection
    conn.close()
