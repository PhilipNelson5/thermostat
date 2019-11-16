#!/usr/bin/env python3

import os
import time

from temperature import readTemp
from flask import render_template
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
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
    return "Furnace on\n"


@app.route('/furnace/off', methods=['POST'])
def furnace_off():
    print("Turning the furnace off")
    return "Furnace off\n"


@app.route('/temperature/up', methods=['POST'])
def temp_up():
    print("Turning temperature up")
    return "turned up\n"


@app.route('/temperature/down', methods=['POST'])
def temp_down():
    print("Turning the temperature down")
    return "turned down\n"


@app.route('/temperature/get', methods=['GET'])
def temp_get():
    print("Getting the temperature")
    return f"{readTemp()}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=False)
