from datetime import datetime
from meteostat import Point, Daily

# Set time period
start = datetime(2018, 1, 1)
end = datetime(2024, 10, 17)

# Create Point for Vancouver, BC
utrecht = Point(52.0907, 5.1214, 0)

# Get daily data for 2018
data = Daily(utrecht, start, end)
data = data.fetch()

data.to_csv("./Datasets/Raw/MeteorologicalFeatures.csv")
