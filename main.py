import time
import sqlite3
from flask import Flask, render_template
import serial
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS


con = sqlite3.connect("weatherData.db")
cur = con.cursor()


sqlCreateTable = """ CREATE TABLE IF NOT EXISTS weather (
                                        utc real PRIMARY KEY,
                                        co2 real,
                                        tvoc real,
                                        temp real,
                                        pressure real,
                                        humidity real,
                                        light real
                                    ); """


cur.execute(sqlCreateTable)
app = Flask(__name__)
    
socketio = SocketIO(app)
CORS(app)


#### GRAB ARDUINO SENSOR VALUES: ##### 

ser = serial.Serial('COM3', 9600) 

data = ser.readline()

weather = data.decode('utf-8').strip().split(',')
utc = int(weather[0])
co2 = float(weather[1])
tvoc = float(weather[2])
temp = float(weather[3])
pressure = float(weather[4])
humidity = float(weather[5])
light = float(weather[6])

weather_tuple = (utc, co2, tvoc, temp, pressure, humidity, light)

cur.execute("INSERT INTO weather VALUES (?, ?, ?, ?, ?, ?, ?);", weather_tuple)
con.commit()


# cur.execute("DELETE FROM weather;")
# con.commit()

def background_task():
    count = 0
    while True:
        socketio.emit('update', {'utc': {utc}, 'co2': {co2},'tvoc': {tvoc},'temp': {temp}, 'pressure': {pressure}, 'humidity': {humidity}, 'light': {light}})
        count += 1
        socketio.sleep(2) 

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})
    socketio.start_background_task(target=background_task)


@app.route('/')
def index():
    return render_template('index.html')

socketio.run(app, debug=True, port=2000)
