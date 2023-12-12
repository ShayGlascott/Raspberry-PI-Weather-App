import base64
import time
import sqlite3
from flask import Flask, jsonify, render_template
import serial
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use Agg backend
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


app = Flask(__name__)
    
socketio = SocketIO(app)
CORS(app)

def background_task():
    count = 0
    while True:
        con = sqlite3.connect("weatherData.db")

        cur = con.cursor()

        cur.execute("SELECT * FROM weather ORDER BY utc DESC LIMIT 1")
        recentData = cur.fetchone()
        if recentData:
            utc, co2, tvoc, temp, pressure, humidity, light = recentData
        else:
            utc = co2 = tvoc = temp = pressure = humidity = light = 0
        cur.close()
        socketio.emit('update', {'utc': utc, 'co2': co2, 'tvoc': tvoc, 'temp': temp, 'pressure': pressure, 'humidity': humidity, 'light': light})
        count += 1
        socketio.sleep(2) 

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})
    socketio.start_background_task(target=background_task)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    conn = sqlite3.connect('weatherData.db')
    cursor = conn.cursor()

    cursor.execute("SELECT utc, co2, tvoc, temp, pressure, humidity, light FROM weather ORDER BY utc DESC ")
    data = cursor.fetchall()

    conn.close()

    columns = ['utc', 'co2', 'tvoc', 'temp', 'pressure', 'humidity', 'light']
    df = pd.DataFrame(data, columns=columns)

    chart_images = {}
    for column in columns[1:]:  
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(df['utc'], df[column], marker='o')
        ax.set_title(f'{column} over Time')
        ax.set_xlabel('UTC Time')
        ax.set_ylabel(column)
        ax.grid(True)

        image_buffer = BytesIO()
        canvas = FigureCanvas(fig)
        canvas.print_png(image_buffer)
        plt.close(fig)

        image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')

        chart_images[column] = f'data:image/png;base64,{image_base64}'

    return render_template('charts.html', chart_images=chart_images)



socketio.run(app, debug=True, port=2000)
