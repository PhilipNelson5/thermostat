#!/usr/bin/env python3

import os
import time

from gpiozero import LED
import sqlite3

from flask import render_template
from flask import Flask
from flask import request
from flask_cors import CORS

import settings
import database

app = Flask(__name__)
cors = CORS(app)

furnace = LED(14)


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
    return f"{{\"temperature\": {settings.desiredTemp}}}"


@app.route('/temperature/down', methods=['POST'])
def temp_down():
    print(f"Turning the temperature down: {settings.desiredTemp}")
    settings.desiredTemp -= 1
    return f"{{\"temperature\": {settings.desiredTemp}}}"


@app.route('/temperature/desired', methods=['GET'])
def temp_get_desired():
    return f"{{\"temperature\": {settings.desiredTemp}}}"


@app.route('/temperature/setdesired/<temp>', methods=['POST'])
def temp_set_desired(temp):
    temp = float(temp)

    if temp != settings.desiredTemp and temp >= settings.minimumSafeTemperature:
        settings.desiredTemp = temp

    return f"{{\"temperature\": {settings.desiredTemp}}}"


@app.route('/temperature/get', methods=['GET'])
def temp_get():
    conn = sqlite3.connect(settings.database)
    c = conn.cursor()
    t = database.getLatestTemp(c)
    if t == None:
        return "{error: \"No temperatures recorded\""

    print(f"Temperature: {t}")
    return f"{{\"temperature\": {t}}}"


@app.route('/schedule/new', methods=['POST'])
def schedule_new():
    start = request.args.get('start', None)
    end =   request.args.get('end', None)
    temp =  request.args.get('temp', None)
    days =  request.args.get('days', None)

    if start is None: return "{error: \"no start specified\"}"
    if end is None:   return "{error: \"no end specified\"}"
    if temp is None:  return "{error: \"no temp specified\"}"
    if days is None:  return "{error: \"no days specified\"}"

    try: start = int(start)
    except: return f"{{error: \"start ({start}) is not an int\"}}"

    try: end = int(end)
    except: return f"{{error: \"end ({end}) is not an int\"}}"

    try: temp = float(temp)
    except: return f"{{error: \"temp ({temp}) is not a float\"}}"

    try: days = int(days)
    except: return f"{{error: \"temp ({days}) is not an int\"}}"

    conn = sqlite3.connect(settings.database)
    c = conn.cursor()
    database.newSchedule(c, start, end, temp, days)
    conn.commit()
    
    return "added new schedule"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
