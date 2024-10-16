import pandas as pd
import numpy as np
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import GridSearchCV, KFold

import xgboost as xgb

from abstractClass import Model


class XGBoost(Model):

    def create_lags(sef, df, target_column):
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

        print(X.shape, Y.shape)
        print(X[0])
        print(Y[0])
        return X, Y

    def create_grid_params(self):
        grid_params = {
            "estimator__n_estimators": [100, 500],
            "estimator__learning_rate": [0.01, 0.05, 0.1],
            "estimator__max_depth": [3, 6, 9],
        }

        return grid_params

    def create_model(self):
        xgboost_model = xgb.XGBRegressor(
            base_score=0.5,
            booster="gbtree",
            objective="reg:squarederror",
            random_state=42,
        )

        multi_output_model = MultiOutputRegressor(xgboost_model)

        return multi_output_model

    def fit_model(self, X_train, y_train, X_val, y_val):
        X_train = np.concatenate([X_train, X_val], axis=0)
        y_train = np.concatenate([y_train, y_val], axis=0)
        hyperparametrs = self.create_grid_params()
        model = self.create_model()

        kf = KFold(n_splits=3, shuffle=False)
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=hyperparametrs,
            cv=kf,
            scoring="neg_mean_squared_error",
            verbose=2,
            n_jobs=-1,
        )

        # Fitting the model with GridSearchCV
        grid_search.fit(X_train, y_train)

        # Extracting the best model
        best_model = grid_search.best_estimator_
        return best_model

    def train_model(self, df, target_column):
        X, y = self.create_lags(df, target_column)
        X_train, X_val, X_test = self.create_splits(X, 0.7, 0.85)
        y_train, y_val, y_test = self.create_splits(y, 0.7, 0.85)

        model = self.fit_model(X_train, y_train, X_val, y_val)
        y_predictions = self.test_model(model, X_test)
        self.print_evaluation_metrics(y_predictions, y_test, target_column)

        return model


df = pd.read_csv("./Data/Datasets/Processed/NO2_features.csv")
xg = XGBoost()
model = xg.train_model(df, "O3")
