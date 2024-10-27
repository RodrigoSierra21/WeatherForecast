import openmeteo_requests
import requests_cache
import pandas as pd

from retry_requests import retry
from datetime import datetime, timedelta


def get_daily_pollutans():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": ["pm10", "pm2_5", "nitrogen_dioxide", "ozone"],
        "start_date": "2024-10-21",
        "end_date": "2024-10-21",
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    hourly = response.Hourly()
    hourly_pm10 = hourly.Variables(0).ValuesAsNumpy()
    hourly_pm2_5 = hourly.Variables(1).ValuesAsNumpy()
    hourly_nitrogen_dioxide = hourly.Variables(2).ValuesAsNumpy()
    hourly_ozone = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["pm10"] = hourly_pm10
    hourly_data["pm2_5"] = hourly_pm2_5
    hourly_data["nitrogen_dioxide"] = hourly_nitrogen_dioxide
    hourly_data["ozone"] = hourly_ozone

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe.set_index("date", inplace=True)
    df = hourly_dataframe.resample("D").mean().round(4)
    df.columns = ["PM2.5", "PM10", "NO2", "O3"]
    df.index = df.index.date

    return df
