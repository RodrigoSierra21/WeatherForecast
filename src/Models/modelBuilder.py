import pandas as pd

from linearRegression import BaselineLinearRegression
from lstm import Lstm
from Xgboost import XGBoost
from randomForest import RandomForest
from Models.abstractClass import Model

# Models for O3
dfO3 = pd.read_csv("./Datasets/Processed/O3_features.csv", index_col=0)
modelO3 = BaselineLinearRegression()
# modelO3 = XGBoost()
# modelO3 = RandomForest()
# modelO3 = Lstm()
modelO3.train_model(dfO3, "O3")


# Models for NO2
# dfNO2 = pd.read_csv("./Datasets/Processed/NO2_features.csv", index_col=0)
# modelNO2 = BaselineLinearRegression()
# modelNO2 = XGBoost()
# modelNO2 = RandomForest()
# modelNO2 = Lstm()
# modelNO2.train_model(dfNO2, "NO2")
