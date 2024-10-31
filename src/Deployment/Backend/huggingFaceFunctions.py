import json
import pandas as pd

from datetime import datetime, timedelta

from DataStreaming.processNewData import new_datapoint_processing_pipeline
from DataMonitoring.dataMonitoring import data_monitoring_pipeline
from DataPrediction.predictNewData import predict_data
from DataPrediction.performanceMonitoring import monitor_metrics


def fetch_data():
    new_datapoint_processing_pipeline()
    data_monitoring_pipeline()


def show_dataDistribution_status():
    with open(
        "./src/Deployment/Data/FeatureInformation/distributionShifts.json", "r"
    ) as file:
        data = json.load(file)

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(list(data.items()), columns=["Feature", "Shift Status"])

    print(df)


def predict_for_O3():
    target_day3 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    predict_data("O3")
    metrics = monitor_metrics("O3", target_day3)
    print(metrics)


def predict_for_NO2():
    target_day3 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    predict_data("NO2")
    metrics = monitor_metrics("NO2", target_day3)
    print(metrics)
