import pandas as pd
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import GridSearchCV, KFold

import xgboost as xgb

from abstractClass import Model


class XGBoost(Model):

    def create_lags(self, df, target_column):

        # Create lag features and targets
        for lag in [1, 2, 3]:
            # Create lagged features for 'o3'
            df[f"{target_column}_lag_{lag}"] = df[target_column].shift(lag)

            if lag <= 3:
                # Create target columns (future values of 'o3')
                df[f"{target_column}_target_{lag}"] = df[target_column].shift(-lag)

        df = df.dropna()

        X = df.drop(
            columns=[
                f"{target_column}_target_{1}",
                f"{target_column}_target_{2}",
                f"{target_column}_target_{3}",
            ]
        )
        y = df[
            [
                f"{target_column}_target_{1}",
                f"{target_column}_target_{2}",
                f"{target_column}_target_{3}",
            ]
        ]

        return X, y

    def create_grid_params(self):
        grid_params = {
            "estimator__n_estimators": [100, 500, 1000],
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
        X_train = pd.concat([X_train, X_val], axis=0)
        y_train = pd.concat([y_train, y_val], axis=0)
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


df = pd.read_csv("./Data/Datasets/Processed/preprocessed_data.csv")
model = XGBoost()
mod = model.train_model(df, 'ozone')
