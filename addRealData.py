
import time
import serial
import sqlite3
#from datetime import datetime

ser = serial.Serial('COM6', baudrate=9600, timeout=1)

con = sqlite3.connect("weatherData.db")
cur = con.cursor()

# sql_create_table = """CREATE TABLE IF NOT EXISTS weather (
#                         utc REAL PRIMARY KEY,
#                         co2 REAL,
#                         tvoc REAL,
#                         temp REAL,
#                         pressure REAL,
#                         humidity REAL,
#                         light REAL
#                     ); """
# cur.execute(sql_create_table)

def insert_data(data):
    sql_insert = """INSERT INTO weather (utc, co2, tvoc, temp, pressure, humidity, light)
                    VALUES (?, ?, ?, ?, ?, ?, ?);"""
    cur.execute(sql_insert, data)
    con.commit()

try:
    time.sleep(10)
    unix_time = int(time.time())
    ser.write(str(unix_time).encode())
    print(f"Sent Unix time: {unix_time}")

    while True:
        data = ser.readline().decode().strip()
        if data:
            data_list = data[1:-1].split(',')
            data_list = [int(data_list[0])] + [float(value) for value in data_list[1:]]
            if len(data_list) == 7:
                insert_data(data_list)
                print(f"Received and saved data: {data_list}")
            else:
                print(f"Ignored data due to incorrect length: {data_list}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Script terminated by user.")
finally:
    ser.close()
    con.close()
