import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam

from abstractClass import Model


class Lstm(Model):
    def create_model(self, X):
        model = Sequential()
        model.add(InputLayer((5, X.shape[2])))
        model.add(LSTM(256, return_sequences=True))
        model.add(LSTM(32))
        model.add(Dropout(0.2))
        model.add(Dense(8, "relu"))
        model.add(Dense(3, "linear"))

        return model

    def fit_model(self, X_train, y_train, X_val, y_val, target_variable):
        model = self.create_model(X_train)
        lr = 0.0002
        model.compile(
            loss=MeanSquaredError(),
            optimizer=Adam(learning_rate=lr),
            metrics=[RootMeanSquaredError()],
        )
        early_stopping_callback = EarlyStopping(
            monitor="val_loss",  # Metric to monitor
            patience=10,  # Number of epochs with no improvement after which training will be stopped
            verbose=1,  # Verbosity mode
            mode="min",  # Mode for the monitored metric
            restore_best_weights=True,  # Restore the weights of the best model
        )

        history = model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            batch_size=32,
            epochs=150,
            callbacks=[early_stopping_callback],
            shuffle=False,
        )

        training_stats = {
            "learning_rate": lr,
            "batch_size": 32,
            "num_epochs": 100,
            "optimizer": "Adam",
            "optimizer_config": {"learning_rate": lr},
            "early_stopping": {
                "patience": early_stopping_callback.patience,
                "monitor": early_stopping_callback.monitor,
                "mode": early_stopping_callback.mode,
                "restore_best_weights": early_stopping_callback.restore_best_weights,
            },
        }

        self.save_training_stats(training_stats, target_variable, "lstm")

        return model, history

    def plot_losses(self, history, target_column):
        # Plot Training vs Validation Loss
        plt.figure(figsize=(12, 5))

        # Plot Loss
        plt.subplot(1, 2, 1)
        plt.plot(history.history["loss"], label="Training Loss")
        plt.plot(history.history["val_loss"], label="Validation Loss")
        plt.title(f"{target_column} Training vs Validation Loss")
        plt.xlabel("Epochs")
        plt.ylabel("Loss")
        plt.legend()

        # Plot MSE (Root Mean Squared Error in this case)
        plt.subplot(1, 2, 2)
        plt.plot(history.history["root_mean_squared_error"], label="Training RMSE")
        plt.plot(
            history.history["val_root_mean_squared_error"], label="Validation RMSE"
        )
        plt.title(f"{target_column} Training vs Validation RMSE")
        plt.xlabel("Epochs")
        plt.ylabel("Root Mean Squared Error")
        plt.legend()

        plt.tight_layout()
        plt.show()

    def train_model(self, df, target_column):
        X, y = self.create_lags(df, target_column)
        num_features = df.shape[1]
        X = X.reshape(X.shape[0], 5, num_features)

        X_train, X_val, X_test = self.create_splits(X, 0.7, 0.85)
        y_train, y_val, y_test = self.create_splits(y, 0.7, 0.85)

        model, history = self.fit_model(X_train, y_train, X_val, y_val, target_column)
        self.plot_losses(history, target_column)
        y_predictions = self.test_model(model, X_test)
        self.print_evaluation_metrics(y_predictions, y_test, target_column)
        self.plot_predictions(y_predictions, y_test, target_column, "LSTM")


df = pd.read_csv("./Datasets/Processed/NO2_features.csv", index_col=0)
lstm = Lstm()
model = lstm.train_model(df, "NO2")
