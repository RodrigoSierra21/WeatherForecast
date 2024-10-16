import pandas as pd
import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, InputLayer, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam

from abstractClass import Model


class Lstm(Model):

    def create_data(self, df, target_column):
        data = df.values
        n_steps = 5
        n_forecast = 3
        X, Y = [], []

        for i in range(len(data) - n_steps - n_forecast + 1):
            X.append(data[i : i + n_steps])
            Y.append(
                data[
                    i + n_steps : i + n_steps + n_forecast,
                    df.columns.get_loc(target_column),
                ]
            )

        X = np.array(X)
        Y = np.array(Y)

        print(X.shape, Y.shape)

        return X, Y

    def create_model(self):
        model = Sequential()
        model.add(InputLayer((5, 11)))
        model.add(LSTM(256, return_sequences=True))
        model.add(LSTM(32))
        model.add(Dropout(0.2))
        model.add(Dense(8, "relu"))
        model.add(Dense(3, "linear"))

        return model

    def fit_model(self, X_train, y_train, X_val, y_val):
        model = self.create_model()
        model.compile(
            loss=MeanSquaredError(),
            optimizer=Adam(learning_rate=0.0002),
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
            epochs=100,
            callbacks=[early_stopping_callback],
            shuffle=False,
        )

        return model, history

    def train_model(self, df, target_column):
        X, y = self.create_data(df, target_column)

        X_train, X_val, X_test = self.create_splits(X, 0.7, 0.85)
        y_train, y_val, y_test = self.create_splits(y, 0.7, 0.85)

        model, _ = self.fit_model(X_train, y_train, X_val, y_val)
        y_predictions = self.test_model(model, X_test)
        self.print_evaluation_metrics(y_predictions, y_test, target_column)


df = pd.read_csv("./Data/Datasets/Processed/O3_features.csv")
lstm = Lstm()
model = lstm.train_model(df, "O3")
