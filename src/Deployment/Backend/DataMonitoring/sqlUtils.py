import sqlite3
import pandas as pd


def get_last_week():
    with sqlite3.connect("./src/Deployment/Data/Databases/pollutionData.db") as conn:
        query = "SELECT * FROM 'Air Pollution Data' ORDER BY rowid DESC LIMIT ?"
        df = pd.read_sql(query, conn, params=(7,))
    return df


def get_features():
    with sqlite3.connect("./src/Deployment/Data/Databases/dataMonitoring.db") as conn:
        query = "SELECT DISTINCT feature FROM data_monitoring;"
        features_df = pd.read_sql(query, conn)

    # Convert the DataFrame column to a list of unique features
    feature_list = features_df["feature"].tolist()
    return feature_list


def get_feature_data(feature, week):
    with sqlite3.connect("./src/Deployment/Data/Databases/dataMonitoring.db") as conn:
        query = """
        SELECT mean_value
        FROM data_monitoring
        WHERE feature = ? AND week_of_year = ?;
        """

        params = (str(feature), str(week))
        df = pd.read_sql(query, conn, params=params)
    return df


def add_all(week, year, values, features):
    with sqlite3.connect("./src/Deployment/Data/Databases/dataMonitoring.db") as conn:
        cursor = conn.cursor()

        # Prepare the SQL statement for inserting/updating values
        sql = """
        INSERT INTO data_monitoring (week_of_year, year, feature, mean_value)
        VALUES (?, ?, ?, ?)
        """

        # Prepare data for executemany
        data_to_insert = [
            (str(week), str(year), feature, value)
            for feature, value in zip(features, values)
        ]

        # Execute the batch insert/update operation
        cursor.executemany(sql, data_to_insert)

        # Commit the transaction
        conn.commit()
