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


def getDesiredTemp() -> Optional[str]:
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
    print("now ",nows)
    # weekday(): monday = 0, sunday = 6
    dow = now.today().weekday()
    # TODO this and how days is stored are backwards...
    mask = 1 << dow
    for start, end, temp, days in schedules:
    #{
        print("checking: ", start, end, temp, bin(days), bin(mask))
        if mask & days != 0 and nows > start and nows < end:
            print("settings temp: ", temp)
            setDesiredTemp(temp)
            return
    #}
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

            if currTemp + settings.buff > desiredTemp:
                turnFurnaceOff()

        #}

        # sleep before the next loop
        time.sleep(settings.sleepIntervalSec)
    #}

if __name__ == "__main__":
    main()
