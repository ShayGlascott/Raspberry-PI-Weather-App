import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database
con = sqlite3.connect("weatherData.db")
cur = con.cursor()

# Insert placeholder data
for _ in range(10):  # Insert 10 rows for example
    # utc = int(datetime.utcnow().timestamp())
    co2 = random.uniform(300, 800)
    tvoc = random.uniform(0, 1)
    temp = random.uniform(20, 30)
    pressure = random.uniform(990, 1010)
    humidity = random.uniform(30, 60)
    light = random.uniform(100, 1000)

    weather_tuple = (co2, tvoc, temp, pressure, humidity, light)

    # Insert data into the weather table
    cur.execute("INSERT INTO weather ( co2, tvoc, temp, pressure, humidity, light) VALUES ( ?, ?, ?, ?, ?, ?);", weather_tuple)

# Commit the changes and close the connection
con.commit()
con.close()