import matplotlib.pyplot as plt
import numpy as np

from scipy import stats


def check_equal_values(df):
    return df["week_of_year"].nunique() == 1


def data_distribution_shift_t_test(value, data):
    data_array = data.to_numpy()

    # Perform one-sample t-test
    t_statistic, p_value = stats.ttest_1samp(data_array, value)

    # Check if p-value is less than the significance level
    return p_value < 0.05


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
