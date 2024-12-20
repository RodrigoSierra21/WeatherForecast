import numpy as np
import pandas as pd
import time

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


from ModelClasses.abstractClass import Model


class BaselineLinearRegression(Model):

    def create_grid_params(self):
        grid_params = {
            "estimator": [Ridge(), Lasso()],
            "estimator__alpha": [0.01, 0.1, 1.0, 10.0],
        }
        return grid_params

    def create_model(self):
        linear_model = LinearRegression()

        # MultiOutputRegressor allows fitting multiple target variables
        multi_output_model = MultiOutputRegressor(linear_model)

        return multi_output_model

    def fit_model(self, X_train, y_train, X_val, y_val, target_variable):
        X_train = np.concatenate([X_train, X_val], axis=0)
        y_train = np.concatenate([y_train, y_val], axis=0)

        hyperparameters = self.create_grid_params()
        model = self.create_model()

        kf = KFold(n_splits=3, shuffle=False)
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=hyperparameters,
            cv=kf,
            scoring="neg_mean_squared_error",
            verbose=2,
            n_jobs=-1,
        )

        start_time = time.time()
        # Fitting the model with GridSearchCV
        grid_search.fit(X_train, y_train)
        training_time = time.time() - start_time

        # Extracting the best model
        best_model = grid_search.best_estimator_

        # Compute training metrics
        y_train_pred = best_model.predict(X_train)
        rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))  # Calculate RMSE
        r2 = r2_score(y_train, y_train_pred)  # Calculate R²
        mae = mean_absolute_error(y_train, y_train_pred)  # Calculate MAE

        # Collect statistics
        training_stats = {
            "best_params": {k: str(v) for k, v in grid_search.best_params_.items()},
            "best_score": float(grid_search.best_score_),
            "rmse": rmse,
            "r2": r2,
            "mae": mae,
            "training_time": training_time,
        }
        self.save_training_stats(training_stats, target_variable, "linearRegression")

        return best_model

    def train_model(self, df, target_column):
        X, y = self.create_lags(df, target_column)
        X_train, X_val, X_test = self.create_splits(X, 0.7, 0.85)
        y_train, y_val, y_test = self.create_splits(y, 0.7, 0.85)
        self.plot_split(df[target_column])
        model = self.fit_model(X_train, y_train, X_val, y_val, target_column)
        y_predictions = self.test_model(model, X_test)
        self.print_evaluation_metrics(y_predictions, y_test, target_column)
        self.plot_predictions(y_predictions, y_test, target_column, "Linear Regression")
