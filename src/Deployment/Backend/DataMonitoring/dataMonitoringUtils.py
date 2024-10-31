import matplotlib.pyplot as plt
import json
import os

from scipy import stats


def check_equal_values(df):
    return df["week_of_year"].nunique() == 1


def plot_histogram(arr):
    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.hist(arr, bins=5, edgecolor="black")  # Plot the histogram
    plt.title("Week mean values")  # Set the title
    plt.xlabel("Mean values")
    plt.grid(axis="y", alpha=0.75)  # Add a grid for better readability
    plt.show()  # Display the plot


def wilcox_test(arr, value):
    differences = arr - value
    _, p_value = stats.wilcoxon(differences[differences != 0])

    return p_value < 0.05


def store_shifts(results):
    file_path = "./src/Deployment/Data/FeatureInformation/distributionShifts.json"

    # Load existing results if the file exists
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            existing_results = json.load(json_file)
    else:
        existing_results = {}

    # Update existing results with the new values
    existing_results.update(results)

    # Write updated results back to the JSON file
    with open(file_path, "w") as json_file:
        json.dump(existing_results, json_file, indent=4)


def plot_distribution_shift(data):
    plt.figure(figsize=(10, 6))  # Optional: Set the figure size
    plt.plot(data, marker="o", linestyle="-", color="b")  # Line plot with markers

    # Adding titles and labels
    plt.title("Line Plot Example")
    plt.xlabel("Year")
    plt.ylabel("Values")

    # Optional: Add grid
    plt.grid()

    # Show the plot
    plt.show()


def alert_data_distribution_shift(feature):
    alerts = []
    with open("./src/Deployment/Data/FeatureInformation/featuresO3.json", "r") as file:
        O3_features = json.load(file)

    with open("./src/Deployment/Data/FeatureInformation/featuresNO2.json", "r") as file:
        NO2_features = json.load(file)

    if feature in NO2_features:
        alerts.append(f"Data distribution shift in {feature}. Retrain NO2 model.")

    if feature in O3_features:
        alerts.append(f"Data distribution shift in {feature}. Retrain O3 model.")

    return alerts
