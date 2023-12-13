import sqlite3
import random
from datetime import datetime, timedelta

con = sqlite3.connect("weatherData.db")
cur = con.cursor()

for _ in range(10): 
    # utc = int(datetime.utcnow().timestamp())
    co2 = random.uniform(300, 800)
    tvoc = random.uniform(0, 1)
    temp = random.uniform(20, 30)
    pressure = random.uniform(990, 1010)
    humidity = random.uniform(30, 60)
    light = random.uniform(100, 1000)

    weather_tuple = (co2, tvoc, temp, pressure, humidity, light)

    cur.execute("INSERT INTO weather ( co2, tvoc, temp, pressure, humidity, light) VALUES ( ?, ?, ?, ?, ?, ?);", weather_tuple)

con.commit()
con.close()