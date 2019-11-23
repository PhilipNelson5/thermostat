from enum import Enum

''' Shared '''
database = "/var/db/thermostat.sqlite"

''' Thermostat '''
sleepIntervalSec = 60

''' Web Server '''
class State(Enum):
    ON = True
    OFF = False

desiredTemp = 70
furnaceState = State.OFF
