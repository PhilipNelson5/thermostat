#!/usr/bin/env python3

import os
import time

from gpiozero import LED
import sqlite3

from flask import render_template
from flask import Flask
from flask_cors import CORS

from temperature import readTemp
import settings

app = Flask(__name__)
cors = CORS(app)

furnace = LED(14)
conn = sqlite3.connect(settings.database)
c = conn.cursor()


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
    if settings.furnaceState != settings.State.ON:
        print("Turning the furnace on")
        settings.furnaceState = settings.State.ON
        furnace.on()
    return "Furnace on"


@app.route('/furnace/off', methods=['POST'])
def furnace_off():
    if settings.furnaceState != settings.State.OFF:
        print("Turning the furnace off")
        settings.furnaceState = settings.State.OFF
        furnace.off()
    return "Furnace off"


@app.route('/temperature/up', methods=['POST'])
def temp_up():
    print(f"Turning temperature up: {settings.desiredTemp}")
    settings.desiredTemp += 1
    return f"{settings.desiredTemp}"


@app.route('/temperature/down', methods=['POST'])
def temp_down():
    print(f"Turning the temperature down: {settings.desiredTemp}")
    settings.desiredTemp -= 1
    return f"{settings.desiredTemp}"


@app.route('/temperature/desired', methods=['GET'])
def temp_desired():
    return f"{settings.desiredTemp}"


@app.route('/temperature/get', methods=['GET'])
def temp_get():
    t = database.getLatestTemp(c)
    if t == None:
        t = 'No temperatures taken'

    print(f"Temperature: {t}")
    return f"{t}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
