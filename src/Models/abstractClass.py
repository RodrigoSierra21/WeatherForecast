import numpy as np
import matplotlib.pyplot as plt
import pickle
import json

from abc import ABC, abstractmethod
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    mean_absolute_error,
    explained_variance_score,
)


# Create an abstract class with the funcitons common to all models
class Model(ABC):

    def create_lags(sef, df, target_column):
        df = df.dropna()
        data = df.values
        n_steps = 5
        n_forecast = 3
        X, Y = [], []

        for i in range(len(data) - n_steps - n_forecast + 1):
            X.append(data[i : i + n_steps].flatten())
            Y.append(
                data[
                    i + n_steps : i + n_steps + n_forecast,
                    df.columns.get_loc(target_column),
                ]
            )

        X = np.array(X)
        Y = np.array(Y)

        return X, Y

    # Creates splits
    def create_splits(self, data, train_percentage=0.7, validation_percentage=0.85):
        train_size = int(len(data) * train_percentage)
        validation_size = int(len(data) * validation_percentage)

        train, validation, test = (
            data[:train_size],
            data[train_size:validation_size],
            data[validation_size:],
        )

        return train, validation, test

    def save_model(self, model, target_column):
        with open(
            f"./src/Deployment/ChampionModels/model{target_column}.pkl", "wb"
        ) as f:
            pickle.dump(model, f)

    def load_model(self, file_path):
        with open(file_path, "rb") as f:
            model = pickle.load(f)

        return model

    def test_model(self, model, X_test):
        y_test_pred = model.predict(X_test)

        return y_test_pred

    def print_evaluation_metrics(self, y_test_pred, y_test, target_variable):
        # Mean Squared Error (MSE) and Root Mean Squared Error (RMSE)
        test_mse = mean_squared_error(y_test, y_test_pred)
        test_rmse = np.sqrt(test_mse)
        test_r2 = r2_score(y_test, y_test_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        explained_variance = explained_variance_score(y_test, y_test_pred)

        print(f"{target_variable} - Test MSE: {test_mse:.4f}")
        print(f"{target_variable} - Test RMSE: {test_rmse:.4f}")
        print(f"{target_variable} - Test MAE: {test_mae:.4f}")
        print(f"{target_variable} - Test R2: {test_r2:.4f}")
        print(f"{target_variable} - Explained Variance: {explained_variance:.4f}")

    def save_training_stats(self, training_stats, target_variable, modelType):
        """Save training statistics to a JSON file."""
        with open(f"./Logs/{target_variable}Logs/{modelType}.json", "w") as f:
            json.dump(training_stats, f, indent=4)

    def plot_predictions(self, y_pred, y_test, target_variable, modelType):

        start_idx = 150
        end_idx = 400

        # Create a figure and three subplots (one for each forecast day)
        fig, axes = plt.subplots(
            3, 1, figsize=(10, 14)
        )  # Increased height for better spacing

        # Plot for Day 1
        axes[0].plot(y_test[start_idx:end_idx, 0], label="Actual Day 1", color="blue")
        axes[0].plot(
            y_pred[start_idx:end_idx, 0],
            label="Predicted Day 1",
            color="red",
            linestyle="--",
        )
        axes[0].set_title(
            f"{target_variable} Test Predictions vs Actuals (Day 1)", fontsize=12
        )  # Adjust title fontsize
        axes[0].set_ylabel(f"{target_variable} Value", fontsize=10)
        axes[0].legend()

        # Plot for Day 2
        axes[1].plot(y_test[start_idx:end_idx, 1], label="Actual Day 2", color="blue")
        axes[1].plot(
            y_pred[start_idx:end_idx, 1],
            label="Predicted Day 2",
            color="red",
            linestyle="--",
        )
        axes[1].set_title(
            f"{target_variable} Test Predictions vs Actuals (Day 2)", fontsize=12
        )  # Adjust title fontsize
        axes[1].set_ylabel(f"{target_variable} Value", fontsize=10)
        axes[1].legend()

        # Plot for Day 3
        axes[2].plot(y_test[start_idx:end_idx, 2], label="Actual Day 3", color="blue")
        axes[2].plot(
            y_pred[start_idx:end_idx, 2],
            label="Predicted Day 3",
            color="red",
            linestyle="--",
        )
        axes[2].set_title(
            f"{target_variable} Test Predictions vs Actuals (Day 3)", fontsize=12
        )  # Adjust title fontsize
        axes[2].set_ylabel(f"{target_variable} Value", fontsize=10)
        axes[2].legend()

        plt.suptitle(
            f"{modelType} {target_variable}", fontsize=16, y=0.98
        )  # Move the title up a bit
        plt.subplots_adjust(hspace=0.4)  # Increase space between subplots

        # Show the plots
        plt.show()

    def plot_split(self, data):
        training_size = int(len(data) * 0.7)  # 70% for training
        validation_size = int(len(data) * 0.15)  # 15% for validation

        # Plot the data splits with different colors and labels
        plt.figure(figsize=(10, 6))

        # Plot training data in blue
        plt.plot(data[:training_size], color="blue", label="Training Data")

        # Plot validation data in orange
        plt.plot(
            range(training_size, training_size + validation_size),
            data[training_size : training_size + validation_size],
            color="orange",
            label="Validation Data",
        )

        # Plot test data in green
        plt.plot(
            range(training_size + validation_size, len(data)),
            data[training_size + validation_size :],
            color="green",
            label="Test Data",
        )

        # Add title and labels
        plt.title("Training, Validation, and Test Data Splits")
        plt.xlabel("Time Steps")
        plt.ylabel("Data Values")

        # Add a legend to distinguish the splits
        plt.legend()

        # Display the plot
        plt.grid(True)
        plt.show()

    @abstractmethod
    def create_model():
        pass

    @abstractmethod
    def fit_model():
        pass

    @abstractmethod
    def train_model():
        pass
