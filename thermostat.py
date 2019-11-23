#!/usr/bin/env python3
import time
import requests
import sqlite3

import settings
import database
from temperature import readTemp

conn = sqlite3.connect(settings.database)

def turnFurnaceOn():
    try:
        r = requests.post('http://localhost:4000/furnace/on')
        print(r.text)
    except:
        pass


def turnFurnaceOff():
    try:
        r = requests.post('http://localhost:4000/furnace/off')
        print(r.text)
    except:
        pass


def getDesiredTemp():
    try:
        r = requests.post('http://localhost:4000/temperature/desired')
        return r.text
    except:
        return None


#if the time is between a and b turn the heater on
def checkTime(a, b):
    currTime = time.localtime()
    if a[0] <= currTime.tm_hour and currTime.tm_hour <= b[0]:
        if a[0] == b[0]:
            if currTime.tm_min >= a[1] and currTime.tm_min <= b[1]:
                return True
        if currTime.tm_min >= a[1] and currTime.tm_min <= 60 and currTime.tm_min <= b[1] and currTime.tm_min >= 0:
            print("Heater on")
            return True


def main():
    c = conn.cursor()
    database.init(c)
    conn.commit()
    buffer = 1
    #Temperture for when we are not home
    defaultTemp = 70
    #Temperture for when we are home

    while True:
        desiredTemp = getDesiredTemp()

	#read the current temp of the room and turn on heater if needed
        currTemp = readTemp()
        database.saveTemperature(c, currTemp)
        conn.commit()
        print(currTemp)

        if desiredTemp is not None:

            if currTemp < defaultTemp:
                turnFurnaceOn()

            else:
                turnFurnaceOff()

            #Turn on heater between a and b
            #The first element in the area is the hour
            #The second element in the area is the minute
            a = [18,32]
            b = [18,32]
            if checkTime(a, b):
                if currTemp < desiredTemp:
                    turnFurnaceOn()

        #makes the program sleep for a specified number of sec
        time.sleep(settings.sleepIntervalSec)

if __name__ == "__main__":
    main()
