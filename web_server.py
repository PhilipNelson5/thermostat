#!/usr/bin/env python3

import os
import time

from temperature import readTemp
from flask import render_template
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

settings = {'desired_temp' : 70,
        'furnace_state' : True }
'''
Modes
    * activate/<mode name>
'''


@app.route('/', methods=['GET'])
def index():
    print("Request for index")
    return render_template('index.html', title='Thermostat')


@app.route('/furnace/on', methods=['POST'])
def furnace_on():
    print("Turning the furnace on")
    settings['furnace_state'] == True
    return "Furnace on\n"


@app.route('/furnace/off', methods=['POST'])
def furnace_off():
    print("Turning the furnace off")
    settings['furnace_state'] == False
    return "Furnace off\n"


@app.route('/temperature/up', methods=['POST'])
def temp_up():
    print(f"Turning temperature up: {settings['desired_temp']}")
    settings['desired_temp'] += 1
    return f"{settings['desired_temp']}"


@app.route('/temperature/down', methods=['POST'])
def temp_down():
    print(f"Turning the temperature down: {settings['desired_temp']}")
    settings['desired_temp'] -= 1
    return f"{settings['desired_temp']}"


@app.route('/temperature/desired', methods=['GET'])
def temp_desired():
    t = readTemp()
    return f"{settings['desired_temp']}"


@app.route('/temperature/get', methods=['GET'])
def temp_get():
    t = readTemp()
    print(f"Temperature: {t}")
    return f"{t}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
