import matplotlib.pyplot as plt
import seaborn as sns


def plot_correlation_matrix(df):
    correlation_matrix = df.corr()

    plt.figure(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Correlation Matrix of All Features")
    plt.show()


# Set the plot style
sns.set_style("whitegrid")


def boxplot_yearly_variation(df):
    # Plot yearly variation for 'no2' and 'o3'
    plt.figure(figsize=(15, 6))
    sns.lineplot(x="year", y=" no2", data=df, label="NO2", color="blue")
    sns.lineplot(x="year", y=" o3", data=df, label="O3", color="orange")
    plt.title("Yearly Variation of NO2 and O3")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.show()


def boxplot_monthly_variation_no2(df):
    # Plot monthly variation for 'no2'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="month", y=" no2", data=df, palette="viridis")
    plt.title("Monthly Variation of NO2")
    plt.xlabel("Month")
    plt.ylabel("NO2 Value")
    plt.show()


def boxplot_monthly_variation_o3(df):
    # Plot monthly variation for 'o3'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="month", y=" o3", data=df, palette="cool")
    plt.title("Monthly Variation of O3")
    plt.xlabel("Month")
    plt.ylabel("O3 Value")
    plt.show()


def boxplot_weekly_variation_no2(df):
    # Plot day of the week variation for 'no2'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="day_of_week", y=" no2", data=df, palette="viridis")
    plt.title("Day of the Week Variation of NO2")
    plt.xlabel("Day of Week (0=Monday, 6=Sunday)")
    plt.ylabel("NO2 Value")
    plt.show()


def boxplot_weekly_variation_o3(df):
    # Plot day of the week variation for 'o3'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="day_of_week", y=" o3", data=df, palette="cool")
    plt.title("Day of the Week Variation of O3")
    plt.xlabel("Day of Week (0=Monday, 6=Sunday)")
    plt.ylabel("O3 Value")
    plt.show()
