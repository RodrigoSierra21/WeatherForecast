import sqlite3
import numpy as np

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from datetime import timedelta, datetime

from DataPrediction.predictUtils import (
    descale_datapoint,
    load_json_file,
)


def get_next_three_days(date):

    date = datetime.strptime(date, "%Y-%m-%d")
    next_days = [(date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 4)]

    return next_days


def get_past_two_days(date):

    date = datetime.strptime(date, "%Y-%m-%d")
    past_days = [(date + timedelta(days=-i)).strftime("%Y-%m-%d") for i in range(1, 3)]

    return past_days


def add_metrics_data(prediction_date, predictions, target_column):
    next_three_days = get_next_three_days(prediction_date)
    predictions = [float(pred) for pred in predictions]

    with sqlite3.connect(
        "./src/Deployment/Data/Databases/metricsMonitoring.db"
    ) as conn:
        cursor = conn.cursor()

        query = f"""
            INSERT INTO {target_column}_prediction_log (prediction_date, target_date1, target_date2, target_date3, predicted_day1, predicted_day2, predicted_day3)
            VALUES (?,?,?,?,?,?,?)
        """

        cursor.execute(
            query,
            (
                prediction_date,
                next_three_days[0],
                next_three_days[1],
                next_three_days[2],
                predictions[0],
                predictions[1],
                predictions[2],
            ),
        )
        conn.commit()


def retrieve_predictions(target_date3, target_column):
    with sqlite3.connect(
        "./src/Deployment/Data/Databases/metricsMonitoring.db"
    ) as conn:
        cursor = conn.cursor()

        # Query to get predictions for the given target_date3
        cursor.execute(
            f"""
            SELECT predicted_day1, predicted_day2, predicted_day3
            FROM {target_column}_prediction_log
            WHERE target_date3 = ?
            """,
            (target_date3,),
        )
        predictions = cursor.fetchone()
        return predictions


def get_ground_truths(target_column, day1, day2, day3):
    with sqlite3.connect("./src/Deployment/Data/Databases/pollutionData.db") as conn:
        cursor = conn.cursor()

        # Use IN (?, ?, ?) to match any of the specified dates
        query = f"""
            SELECT {target_column}
            FROM [Air Pollution Data]
            WHERE DateTime IN (?, ?, ?)
        """

        cursor.execute(query, (day1, day2, day3))

        ground_truths = [row[0] for row in cursor.fetchall()]

    return np.array(ground_truths)


def get_metrics(predictions, ground_truths):
    predictions = np.array(predictions)
    ground_truths = np.array(ground_truths)

    # Calculate RMSE
    rmse = np.sqrt(mean_squared_error(ground_truths, predictions))

    # Calculate R²
    r2 = r2_score(ground_truths, predictions)

    # Calculate MAE
    mae = mean_absolute_error(ground_truths, predictions)

    return {"RMSE": rmse, "R²": r2, "MAE": mae}


def monitor_metrics(target_column, target_date3):

    # Retrieve the last predictions with ground truths
    predictions = retrieve_predictions(target_date3, target_column)

    # Get the past to days to retrieve teh values from the dataset
    past_days = get_past_two_days(target_date3)

    # Retrieve the ground truths values
    ground_truths = get_ground_truths(
        target_column, target_date3, past_days[1], past_days[0]
    )

    # De scale ground truth values
    feature_info = load_json_file()
    min_max_values = feature_info.get("min_max", {})
    ground_truths = descale_datapoint(ground_truths, min_max_values, target_column)
    ground_truths = ground_truths.values
    ground_truths = ground_truths.flatten()

    # Compute the most recent metrics
    metrics = get_metrics(predictions, ground_truths)

    return metrics
