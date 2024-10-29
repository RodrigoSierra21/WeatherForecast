import matplotlib.pyplot as plt
import seaborn as sns

# Set the plot style
sns.set_style("whitegrid")


# Plot correlation matrix
def plot_correlation_matrix(df):
    correlation_matrix = df.corr()

    plt.figure(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Correlation Matrix of All Features")
    plt.show()


def boxplot_yearly_variation(df):
    # Plot yearly variation for 'no2' and 'o3'
    plt.figure(figsize=(15, 6))
    sns.lineplot(x="year", y="NO2", data=df, label="NO2", color="blue")
    sns.lineplot(x="year", y="O3", data=df, label="O3", color="orange")
    plt.title("Yearly Variation of NO2 and O3")
    plt.xlabel("Year")
    plt.ylabel("Value")
    plt.legend()
    plt.show()


def boxplot_monthly_variation_no2(df):
    # Plot monthly variation for 'no2'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="month", y="NO2", data=df, palette="viridis")
    plt.title("Monthly Variation of NO2")
    plt.xlabel("Month")
    plt.ylabel("NO2 Value")

    # Make x-axis cleaner by reducing ticks and rotating labels
    plt.xticks(
        ticks=range(0, 12),
        labels=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        rotation=45,
    )

    plt.tight_layout()
    plt.show()


def boxplot_monthly_variation_o3(df):
    # Plot monthly variation for 'o3'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="month", y="O3", data=df, palette="cool")
    plt.title("Monthly Variation of O3")
    plt.xlabel("Month")
    plt.ylabel("O3 Value")

    # Make x-axis cleaner by reducing ticks and rotating labels
    plt.xticks(
        ticks=range(0, 12),
        labels=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        rotation=45,
    )

    plt.tight_layout()
    plt.show()


def boxplot_weekly_variation_no2(df):
    # Plot day of the week variation for 'no2'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="day_of_week", y="NO2", data=df, palette="viridis")
    plt.title("Day of the Week Variation of NO2")
    plt.xlabel("Day of Week")
    plt.ylabel("NO2 Value")

    # Make x-axis cleaner by using day names instead of numbers
    plt.xticks(
        ticks=range(0, 7), labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )

    plt.tight_layout()
    plt.show()


def boxplot_weekly_variation_o3(df):
    # Plot day of the week variation for 'o3'
    plt.figure(figsize=(15, 6))
    sns.boxplot(x="day_of_week", y="O3", data=df, palette="cool")
    plt.title("Day of the Week Variation of O3")
    plt.xlabel("Day of Week")
    plt.ylabel("O3 Value")

    # Make x-axis cleaner by using day names instead of numbers
    plt.xticks(
        ticks=range(0, 7), labels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )

    plt.tight_layout()
    plt.show()


def plot_histograms(df):
    # Plot histograms for all numeric variables
    df.hist(figsize=(15, 12), bins=20, edgecolor="black")
    plt.suptitle("Histograms of All Variables", fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
