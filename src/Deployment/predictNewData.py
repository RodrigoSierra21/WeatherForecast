import pandas as pd

from predictUtils import (
    load_features,
    get_rows,
    scale_datapoint,
    load_json_file,
    load_champion_model,
)


def predict_data():

    # Retrieve the last five days
    last_datapoint = get_rows(5)
    print(last_datapoint)

    # De scale predictions
    feature_info = load_json_file()
    print(feature_info)
    min_max_values = feature_info.get("min_max", {})

    # Select features for O3
    # O3_features = load_features("O3")
    # O3_df = last_datapoint[O3_features]

    # Load model for O3
    # model = XGBoost()
    # model.load_model("./path")

    # Do predictions for O3
    # O3_datapoint = O3_df.to_numpy().reshape(1, 5, 5)  # Reshape to (1, 5, 5)
    # O3_datapoint = O3_datapoint.flatten()
    # pred_O3 = model.predict(O3_datapoint)

    # De scale predictions

    # Return predictions

    # Select features for NO2
    NO2_features = load_features("NO2")
    print(NO2_features)
    NO2_df = last_datapoint[NO2_features]
    print(NO2_df)

    # Load model for NO2
    model = load_champion_model("./ChampionModels/modelNO2.pkl")

    # Do predictions for NO2
    NO2_datapoint = NO2_df.to_numpy().reshape(1, 5, 10)
    NO2_datapoint = NO2_datapoint.flatten()
    pred_NO2 = model.predict(NO2_datapoint)
    predictions = scale_datapoint(pred_NO2, min_max_values, "NO2")
    print(predictions)

    # Return predictions


predict_data()
