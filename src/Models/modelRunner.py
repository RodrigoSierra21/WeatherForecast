from ModelClasses.linearRegression import BaselineLinearRegression
from ModelClasses.Xgboost import XGBoost
from ModelClasses.lstm import Lstm
from ModelClasses.randomForest import RandomForest


target_column = "O3"
# target_column = "NO2"
# model = XGBoost()
# model = Lstm()
# model = RandomForest()
model = BaselineLinearRegression()
df = model.load_data(target_column)
model.train_model(df, target_column)
