import sqlite3
import pandas as pd


def get_data():
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
    df = pd.read_sql(f"SELECT {', ' .join(columns)} FROM [{table_name}]", conn)

    conn.close()

    return df


def create_table(feature, data):
    weekly_mean = data.groupby(["year", "week_of_year"])[feature].mean().reset_index()

    df = weekly_mean.pivot(index="week_of_year", columns="year", values=feature)
    df.reset_index(inplace=True)

    return df


def createDataDistributionShitfDatabase():

    df = get_data()
    features = df.drop(columns=["year", "week_of_year"])
    labels = df[["year", "week_of_year"]]
    conn = sqlite3.connect("./Datasets/Databases/DataDistributionShiftDatabase.db")

    for feature in features.columns:
        data = pd.concat([features[feature], labels], axis=1)

        table = create_table(feature, data)
        table.to_sql(feature, conn, if_exists="replace", index=False)

        data.drop(columns=[feature])

    conn.commit()
    conn.close()


createDataDistributionShitfDatabase()
