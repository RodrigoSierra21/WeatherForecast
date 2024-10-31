from datetime import datetime, timedelta
from meteostat import Point, Daily


def get_daily_meteorological():
    # Set time period
    yesterday = datetime.combine(
        datetime.today() - timedelta(days=1), datetime.min.time()
    )
    today = datetime(2024, 10, 28)
    tod = datetime(2024, 10, 30)

    # Create Point for Utretch
    utrecht = Point(52.0907, 5.1214, 0)

    # Get daily data for 2018
    data = Daily(utrecht, today, tod)
    data = data.fetch()
    data.index = data.index.date

    return data
