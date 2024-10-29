from DataProcessing.processNewData import new_datapoint_processing_pipeline
from DataMonitoring.dataMonitoring import data_monitoring_pipeline


def main():
    new_datapoint_processing_pipeline()
    data_monitoring_pipeline()


if __name__ == "__main__":
    main()
