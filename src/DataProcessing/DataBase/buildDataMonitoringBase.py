import sqlite3
import pandas as pd


def get_data():
    # Connect with teh database
    conn = sqlite3.connect("./Datasets/Databases/pollutionDataBase.db")

    table_name = "Air Pollution Data"
    columns = [
        "NO2",
        '"PM2.5"',
        "PM10",
        "O3",
        "tavg",
        "prcp",
        "wdir",
        "wspd",
        "pres",
        "year",
        "week_of_year",
    ]

    # Select only the features used for model training
    df = pd.read_sql(f"SELECT {', ' .join(columns)} FROM [{table_name}]", conn)

    # Close the connection
    conn.close()

    return df


def create_database():

    # Create teh database for data distribution shifts
    with sqlite3.connect("./src/Deployment/Data/Databases/dataMonitoring.db") as conn:
        cursor = conn.cursor()

        # Set the week of the year, year and feature to primary keys for easier access
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data_monitoring (
                week_of_year INTEGER,
                year INTEGER,
                feature TEXT,
                mean_value REAL,
                PRIMARY KEY (week_of_year, year, feature)
            );
        """
        )
        # Indexing for faster querying (useful for frequent retrievals by feature/year/week_of_year)
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_week_year_feature ON data_monitoring (week_of_year, year, feature);"
        )
        conn.commit()


def bulk_insert_data(data):
    # Example input: data is a list of tuples, e.g., [(week, year, feature, mean_value), ...]
    with sqlite3.connect("./src/Deployment/Data/Databases/dataMonitoring.db") as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO data_monitoring (week_of_year, year, feature, mean_value)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (week_of_year, year, feature) DO UPDATE SET mean_value = excluded.mean_value
            """,
            data,
        )
        conn.commit()


def transform_to_tuple_format(df):
    # Group by 'year' and 'week_of_year', then calculate mean for each feature
    grouped = df.groupby(["year", "week_of_year"]).mean().reset_index()

    # Prepare a list of tuples in the desired format
    result = []
    for _, row in grouped.iterrows():
        year = row["year"]
        week = row["week_of_year"]
        for feature in df.columns.drop(["year", "week_of_year"]):
            mean_value = row[feature]
            result.append((week, year, feature, mean_value))

    return result


def buildDataMonitoringBase():

    create_database()
    df = get_data()
    df = transform_to_tuple_format(df)
    bulk_insert_data(df)


# buildDataMonitoringBase()
