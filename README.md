# Raspberry-Pi Weather App


The project features a smart weather station with a Raspberry Pi serving as the base station. The Raspberry Pi hosts a dedicated website and collects sensor data transmitted 
from an Arduino located outdoors using XBee transmitters. This setup allows users to access both real-time weather data and historical trends stored on the Raspberry Pi.

The system utilizes sensors to measure light level, pressure, temperature, humidity, and air quality. These sensor readings are presented in graph format on the web application, 
providing a user-friendly interface for monitoring and analyzing current weather conditions and trends.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

git clone https://github.com/your-username/your-project.git
cd your-project
npm install

### Dependencies (Not pre installed on Raspberry Pi 3v+)

- [flask-socketio]
- [flask-cors]
- [pandas]

