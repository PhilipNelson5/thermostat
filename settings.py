from enum import Enum

''' Shared '''
database = "/var/db/thermostat.sqlite"
minimumSafeTemperature = 50

''' Thermostat '''
buff = 3
sleepIntervalSec = 60
webserver = 'localhost:4000'

''' Web Server '''
class State(Enum):
    ON = True
    OFF = False

desiredTemp = 70
furnaceState = State.OFF
