from datetime import datetime, timedelta
from meteostat import Point, Daily


def get_daily_meteorological():
    # Set time period
    yesterday = datetime(2024, 10, 21)

    # Create Point for Vancouver, BC
    utrecht = Point(52.0907, 5.1214, 0)

    # Get daily data for 2018
    data = Daily(utrecht, yesterday, yesterday)
    data = data.fetch()
    data.index = data.index.date

    return data
