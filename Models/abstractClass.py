import numpy as np
import pickle
from abc import ABC, abstractmethod
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, explained_variance_score


# Create an abstract class with the funcitons common to all models
class Model(ABC):

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

    def save_model(self, model):
        with open("./src/models/savedModels", "wb") as f:
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

    @abstractmethod
    def create_model():
        pass

    @abstractmethod
    def fit_model():
        pass

    @abstractmethod
    def train_model():
        pass
