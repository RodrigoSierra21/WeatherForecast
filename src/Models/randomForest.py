import pandas as pd
import numpy as np
import time

from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from abstractClass import Model


class RandomForest(Model):
    def create_grid_params(self):
        grid_params = {
            "estimator__n_estimators": [150, 300],
            "estimator__max_depth": [15, 30],
            "estimator__min_samples_split": [2, 5, 10],
            "estimator__min_samples_leaf": [
                1,
                2,
                4,
            ],
            "estimator__max_features": [
                "sqrt",
                "log2",
            ],
        }

        return grid_params

    def create_model(self):
        model = RandomForestRegressor(random_state=42)
        model = MultiOutputRegressor(model)

        return model

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
        self.save_training_stats(training_stats, target_variable, "randomForest")

        return best_model

    def train_model(self, df, target_column):
        X, y = self.create_lags(df, target_column)
        X_train, X_val, X_test = self.create_splits(X, 0.7, 0.85)
        y_train, y_val, y_test = self.create_splits(y, 0.7, 0.85)
        model = self.fit_model(X_train, y_train, X_val, y_val, target_column)
        y_predictions = self.test_model(model, X_test)

        # Uncomment to print evaluation metrics and plots
        # self.print_evaluation_metrics(y_predictions, y_test, target_column)
        # self.plot_predictions(y_predictions, y_test, target_column, "Random Forest")

        return model


df = pd.read_csv("./Datasets/Processed/NO2_features.csv", index_col=0)
rf = RandomForest()
model = rf.train_model(df, "NO2")
