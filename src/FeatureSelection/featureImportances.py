import pandas as pd

from featureImportancesUtil import (
    create_lags,
    create_splits,
    fit_model,
    plot_feature_importances,
    compute_importances,
    drop_features,
    save_features,
)


df = pd.read_csv("./Datasets/Processed/preprocessed_data.csv")
target_column = "NO2"
# target_column = "O3"

X = df.to_numpy()
X = X[3:-4]
y = create_lags(df, target_column)
X_train, X_val, X_test = create_splits(X, 0.7, 0.85)
y_train, y_val, y_test = create_splits(y, 0.7, 0.85)

model = fit_model(X_train, y_train, X_val, y_val, target_column)
importances = compute_importances(model, df.columns.tolist())
plot_feature_importances(importances, target_column, 0.05)

kept_features = drop_features(importances, 0.05)
df = df[kept_features]
save_features(kept_features, target_column)

df.to_csv("./Datasets/Processed/NO2_features.csv")