import sqlite3

from getData import get_table_names


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


def craft_update_query(table_name, year):
    update_query = f"""
        UPDATE "{table_name}" 
        SET "{year}" = ? 
        WHERE "week_of_year" = ? AND "{year}" IS NULL
        """
    return update_query


def addDistributionShiftValue(data):

    conn = sqlite3.connect("./Datasets/DataBases/DataDistributionShiftDatabase.db")
    table_names = get_table_names(conn)

    week_of_year = data["week_of_year"].iloc[0]
    year = data["year"].iloc[0]
    data = data[[col for col in data.columns if col in table_names]]

    for feature in data.columns:
        mean_value = data[feature].mean()
        query = craft_update_query(feature, year)
        cursor = conn.cursor()
        cursor.execute(query, (mean_value, week_of_year))

    conn.commit()
    cursor.close()
    conn.close()
