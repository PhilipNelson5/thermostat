def readTemp():
    f = open("/sys/bus/w1/devices/28-01187a672bff/w1_slave", "r")
    lines = f.readlines()
    f.close

    temp = lines[1].find("t=")
    if temp != -1:
        temp_string = lines[1].strip()[temp+2:]
        tempC = float(temp_string) / 1000.0
        tempF = tempC * 9.0 / 5.0 + 32.0

    return tempF
