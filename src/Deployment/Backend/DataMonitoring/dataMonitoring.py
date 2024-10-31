from DataMonitoring.dataMonitoringUtils import (
    check_equal_values,
    plot_histogram,
    wilcox_test,
    store_shifts,
    alert_data_distribution_shift,
)

from DataMonitoring.sqlUtils import (
    get_last_week,
    get_feature_data,
    get_features,
    add_all,
)


def data_monitoring_pipeline():
    last_week_data = get_last_week()
    if check_equal_values(last_week_data):

        # Get the current week of the year
        week_of_year = last_week_data["week_of_year"].iloc[0]
        year = last_week_data["year"].iloc[0]
        values_to_add = []
        alerts = []
        shifts = {}
        features = get_features()
        for feature in features:
            values = get_feature_data(feature, week_of_year)["mean_value"].to_numpy()
            value = last_week_data[feature].mean()
            values_to_add.append(value)
            # Determine if the data is normally distributed
            # plot_histogram(rows)

            flag = bool(wilcox_test(values, value))

            # There has been a data distribution shift
            if flag:
                alerts.extend(alert_data_distribution_shift(feature))

            shifts[feature] = flag

        add_all(week_of_year, year, values_to_add, features)
        store_shifts(shifts)
        return alerts

    else:
        return None
