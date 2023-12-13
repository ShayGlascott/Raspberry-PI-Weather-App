# Raspberry-Pi Weather App

The project features a smart weather station with a Raspberry Pi serving as the base station. The Raspberry Pi hosts a dedicated website and collects sensor data transmitted 
from an Arduino located outdoors using XBee transmitters. This setup allows users to access both real-time weather data and historical trends stored on the Raspberry Pi.

The system utilizes sensors to measure light level, pressure, temperature, humidity, and air quality. These sensor readings are presented in graph format on the web application, 
providing a user-friendly interface for monitoring and analyzing current weather conditions and trends.

## Table of Contents

- [Usage](#usage)

## Usage

To set up and use the smart weather station, follow these steps:

### 1. Hardware Setup

- Connect the Raspberry Pi to power and ensure it has internet connectivity.
- Place the Arduino outdoors with the connected sensors for optimal data collection.
- Make sure the XBee transmitters are properly configured and connected to both the Arduino and Raspberry Pi.

### 2. Software Installation

### Dependencies (Not pre installed on Raspberry Pi 3v+)

sudo apt install...
- [flask-socketio]
- [flask-cors]
- [pandas]


- Clone the project repository to your Raspberry Pi:
  - git clone https://github.com/ShayGlascott/Raspberry-PI-Weather-App.git
  - cd Raspberry-PI-Weather-App
   

- Find COM port on Raspberry Pi and change comPort variable in "addRealData.py"
- Run "python3 main.py"
- Open a new terminal window and run "python3 addRealData.py"
  


