import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor


class RandomForestFeatureSelection:
    def create_lags(self, df):
        # Create lag features and targets
        for lag in [1, 2, 3]:
            # Create target columns (future values of 'o3')
            df[f"o3_target_{lag}"] = df["O3"].shift(-lag)

        df = df.dropna()

        X = df.drop(columns=[f"o3_target_{1}", f"o3_target_{2}", f"o3_target_{3}"])
        y = df[[f"o3_target_{1}", f"o3_target_{2}", f"o3_target_{3}"]]

        return X, y

    def create_splits(self, data, train_percentage=0.7, validation_percentage=0.85):
        train_size = int(len(data) * train_percentage)
        validation_size = int(len(data) * validation_percentage)

        train, validation, test = (
            data[:train_size],
            data[train_size:validation_size],
            data[validation_size:],
        )

        return train, validation, test

    def create_grid_params(self):
        grid_params = {
            "estimator__n_estimators": [150, 300],
            "estimator__max_depth": [15, 30],
            "estimator__min_samples_split": [2, 5, 10],
            "estimator__min_samples_leaf": [
                1,
                2,
                # 4,
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

    def fit_model(self, X_train, y_train, X_val, y_val):
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

        # Fitting the model with GridSearchCV
        grid_search.fit(X_train, y_train)

        # Extracting the best model
        best_model = grid_search.best_estimator_
        return best_model

    def plot_feature_importances(self, model, X, target_column):
        # Averaging the feature importances across the multi-output model
        importances = np.mean(
            [est.feature_importances_ for est in model.estimators_], axis=0
        )

        feature_names = X.columns.tolist()

        # Sorting the features by importance
        indices = np.argsort(importances)[::-1]

        # Plotting the feature importances
        plt.figure(figsize=(10, 6))
        plt.title(f"Feature Importances {target_column}")
        plt.bar(range(len(importances)), importances[indices], align="center")
        plt.xticks(
            range(len(importances)), [feature_names[i] for i in indices], rotation=90
        )
        plt.tight_layout()
        plt.show()

    def train_model(self, df, target_column):
        X, y = self.create_lags(df)
        X_train, X_val, X_test = self.create_splits(X, 0.7, 0.85)
        y_train, y_val, y_test = self.create_splits(y, 0.7, 0.85)

        model = self.fit_model(X_train, y_train, X_val, y_val)
        self.plot_feature_importances(model, X, target_column)

        return model


df = pd.read_csv("./Data/Datasets/Processed/preprocessed_data_all.csv")
# rf_for_frature_selection = RandomForestFeatureSelection()
# model = rf_for_frature_selection.train_model(df, "O3")

print(df.columns)
df = df.drop(
    columns=[
        "prcp",
        "snow",
        "month",
        "day",
        "day_of_week",
        "week_of_year",
        "is_spring",
        "is_summer",
        "is_autumn",
        "is_winter",
    ]
)

df.to_csv("./Data/Datasets/Processed/NO2_features.csv")
