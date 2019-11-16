#!/usr/bin/env python3
import time
from temperature import readTemp
from gpiozero import LED

#status is a bool that shows if you want the power on or off
heater = LED(14)


def power(status):
    if status: 
        heater.on()
        #print("Heater on")
        
    else:
        heater.off()
        #print("Heater off")


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
    sec = 3
    buffer = 1
    #Temperture for when we are not home
    defaultTemp = 77
    #Temperture for when we are home
    desiredTemp = 85

    while True:

        #read the current temp of the room and turn on heater if needed
        currTemp = readTemp()
        print(currTemp)

        if currTemp < defaultTemp:
            power(True)

        else:
            power(False)
        
        #Turn on heater between a and b 
        #The first element in the area is the hour
        #The second element in the area is the minute 
        a = [14,9]
        b = [14,10]
        if checkTime(a, b):
            if currTemp < desiredTemp:
                power(True)

        #makes the program sleep for a specified number of sec
        time.sleep(sec)

if __name__ == "__main__":
    main()