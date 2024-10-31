import sqlite3

# Create the database for data distribution shifts
with sqlite3.connect("./src/Deployment/Data/Databases/metricsMonitoring.db") as conn:
    cursor = conn.cursor()

    # Create table for O3 predictions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS O3_prediction_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_date DATE NOT NULL,
            target_date1 DATE,
            target_date2 DATE,
            target_date3 DATE,
            predicted_day1 FLOAT,
            predicted_day2 FLOAT,
            predicted_day3 FLOAT
        );
        """
    )

    # Create table for NO2 predictions
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS NO2_prediction_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_date DATE NOT NULL,
            target_date1 DATE,
            target_date2 DATE,
            target_date3 DATE,
            predicted_day1 FLOAT,
            predicted_day2 FLOAT,
            predicted_day3 FLOAT
        );
        """
    )

    # Commit the changes
    conn.commit()
