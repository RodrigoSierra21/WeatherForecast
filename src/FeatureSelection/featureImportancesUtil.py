import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import time

from sklearn.model_selection import GridSearchCV, KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# Log training statistics
def save_training_stats(training_stats, target_variable):
    """Save training statistics to a JSON file."""
    with open(f"./Logs/FeatureImportanceLogs/{target_variable}training.json", "w") as f:
        json.dump(training_stats, f, indent=4)


# Create the target variable
def create_lags(df, target_column):
    data = df.values
    n_steps = 5
    n_forecast = 3
    Y = []

    for i in range(len(data) - n_steps - n_forecast + 1):
        Y.append(
            data[
                i + n_steps : i + n_steps + n_forecast,
                df.columns.get_loc(target_column),
            ]
        )

    Y = np.array(Y)

    return Y


# Create the data splits for training testing and validation
def create_splits(data, train_percentage=0.7, validation_percentage=0.85):
    train_size = int(len(data) * train_percentage)
    validation_size = int(len(data) * validation_percentage)

    train, validation, test = (
        data[:train_size],
        data[train_size:validation_size],
        data[validation_size:],
    )

    return train, validation, test


# Hyperparameter grid for gridsearch
def create_grid_params():
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


# Create teh random forest model
# Wrap it with multioutput to predict multiple days
def create_model():
    model = RandomForestRegressor(random_state=42)
    model = MultiOutputRegressor(model)

    return model


# train the model and log statistics
def fit_model(X_train, y_train, X_val, y_val, target_variable):
    X_train = np.concatenate([X_train, X_val], axis=0)
    y_train = np.concatenate([y_train, y_val], axis=0)

    # Get hyperperparameter grid
    hyperparameters = create_grid_params()

    # Create the model
    model = create_model()

    # Perform grid search
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
        "best_params": grid_search.best_params_,
        "best_score": grid_search.best_score_,
        "cv_results": {
            "mean_test_score": grid_search.cv_results_["mean_test_score"].tolist(),
            "params": grid_search.cv_results_["params"],
        },
        "rmse": rmse,
        "r2": r2,
        "mae": mae,
        "training_time": training_time,
    }

    save_training_stats(training_stats, target_variable)

    return best_model


# Compute the feature importances
def compute_importances(model, feature_names):
    importances = np.mean(
        [est.feature_importances_ for est in model.estimators_], axis=0
    )
    feature_importances_df = pd.DataFrame(
        {"Feature": feature_names, "Importance": importances}
    )

    # Sort the DataFrame by importance
    feature_importances_df = feature_importances_df.sort_values(
        by="Importance", ascending=False
    )

    return feature_importances_df


def plot_feature_importances(df, target_column, threshold):
    plt.figure(figsize=(10, 6))
    plt.barh(df["Feature"], df["Importance"], color="skyblue")
    plt.axvline(
        x=threshold, color="red", linestyle="--", label=f"Threshold = {threshold}"
    )
    plt.xlabel("Importance")
    plt.title(f"Feature Importances {target_column}")
    plt.gca().invert_yaxis()  # Invert y-axis to have the most important feature on top
    plt.tight_layout()
    plt.show()


# Drop non important features (all below the threshold)
def drop_features(importances, threshold):
    retained_features_df = importances[importances["Importance"] >= threshold]

    # Extract the retained feature names as a NumPy array
    retained_features = retained_features_df["Feature"].to_numpy()

    return retained_features


def save_features(features, target_column):
    with open(
        f"./Datasets/FeatureInformation/features{target_column}.json", "w"
    ) as json_file:
        json.dump(features.tolist(), json_file)
