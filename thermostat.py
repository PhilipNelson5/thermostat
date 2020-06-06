#!/usr/bin/env python3

from typing import List, Set, Dict, Tuple, Optional
from datetime import datetime

import json
import time
import requests
import sqlite3

import settings
import database
from temperature import readTemp

conn = sqlite3.connect(settings.database)

def turnFurnaceOn() -> None:
    try:
        r = requests.post(f'http://{settings.webserver}/furnace/on')
        print(r.text)
    except:
        pass


def turnFurnaceOff() -> None:
    try:
        r = requests.post(f'http://{settings.webserver}/furnace/off')
        print(r.text)
    except:
        pass


def getDesiredTemp() -> Optional[float]:
    try:
        r = requests.get(f'http://{settings.webserver}/temperature/desired')
        try:
            res = json.loads(r.text)
            return float(res['temperature'])
        except:
            print(f"error: {r.text} can not be parsed")
    except:
        return None


def setDesiredTemp(temp) -> None:
    try:
        r = requests.post(f'http://{settings.webserver}/temperature/setdesired/{temp}')
    except:
        pass


def checkSchedules(c: sqlite3.Cursor) -> None:
    schedules = database.getSchedules(c)
    if schedules is None: return

    now = datetime.now()
    nows = now.hour*3600 + now.minute*60 + now.second

    # weekday(): monday = 0, sunday = 6
    # dow:       monday = 6, sunday = 0
    dow = 6 - now.today().weekday()

    # mask:      monday = 0b1000000
    #            sunday = 0b0000001
    mask = 1 << dow

    for start, end, temp, days in schedules:
    #{
        print("checking schedule: ", start, end, temp, bin(days), bin(mask))
        if mask & days == mask and nows > start and nows < end:
            print("settings temp: ", temp)
            setDesiredTemp(temp)
            return
    #}

    print("no active schedules")
    setDesiredTemp(settings.minimumSafeTemperature)


def main():
    c = conn.cursor()
    database.init(c)
    conn.commit()

    while True:
    #{
        checkSchedules(c)
        desiredTemp = getDesiredTemp()

        currTemp = readTemp()
        database.saveTemperature(c, currTemp)
        conn.commit()
        print(currTemp)

        # if there is a response from the web server
        if desiredTemp is not None:
        #{

            if currTemp < desiredTemp:
                turnFurnaceOn()

            elif currTemp + settings.buff > desiredTemp:
                turnFurnaceOff()

        #}

        # sleep before the next loop
        time.sleep(settings.sleepIntervalSec)
    #}

if __name__ == "__main__":
    main()
