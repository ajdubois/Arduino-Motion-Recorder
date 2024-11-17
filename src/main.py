import math
from time import sleep
from time import time
from engi1020.arduino.api import *
from engi1020.arduino.pressure import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


maxAnalogValue = 1023


        

def collectSampleAccelerationX():
    return three_axis_get_accelX()
    
def collectSampleAccelerationY():
    return three_axis_get_accelY()
    
def collectSampleAccelerationZ():
    return three_axis_get_accelZ()
    

def setLED(activated):
    digital_write(4, activated)

def isButtonPressed():
    return digital_read(6)
    
xAxisEnabled = True
yAxisEnabled = False
zAxisEnabled = False

def getAxisCount():
    return xAxisEnabled + yAxisEnabled + zAxisEnabled
    

def getRotaryDialValue():
    return analog_read(0)

def linearDialFunction(min, max):
    dialValue = getRotaryDialValue()
    slope = (max - min) / maxAnalogValue
    return slope * dialValue + min



sampleInterval = 0.01 # Interval in seconds between sample collection.



# Delay is the delay before the start of data collection in seconds.
def collectDataUntilButtonPress(delay):
    sleep(delay)
    startTime = time()
    
    data_dictX = {}


    setLED(True)
    while not isButtonPressed():
        sleep(sampleInterval)

        data_dictX[time() - startTime] = collectSampleAccelerationX() * 9.81 # in m/s

    setLED(False)
    return data_dictX
    
    
def oled_update(text):
    oled_clear()
    oled_print(text)
    
    
    
    


# Set mode

mode = "timer" # can be "timer" or "button".

if getRotaryDialValue() > maxAnalogValue / 2:
    mode = "timer"
else:
    mode = "button"

lastMode = mode # only update oled display when mode changes
 


oled_update("Select desired mode.")
sleep(5)

oled_update(mode)

while not isButtonPressed():
    sleep(0.5)
    
    dialValue = getRotaryDialValue()
    
    if dialValue > maxAnalogValue / 2:
        mode = "timer"
        if lastMode != mode:
            oled_update("timer")
    else:
        mode = "button"
        if lastMode != mode:
            oled_update("button")
    lastMode = mode
        
oled_update(mode + " mode selected.")
sleep(2)



# get delay


oled_update("Choose delay...")
sleep(2.5)

delay = 1
lastDelay = -99

while not isButtonPressed():
    sleep(0.15)
    delay = math.ceil(linearDialFunction(1, 30))
    
    if delay != lastDelay:
        oled_update(str(delay))
    lastDelay = delay
    
        
oled_update(str(delay) + " second delay.")
sleep(3)


# get timer

oled_update("Timer duration...")
sleep(2.5)

if mode == "timer":
    duration = 5
    lastDuration = -99

    while not isButtonPressed():
        sleep(0.15)
        duration = math.ceil(linearDialFunction(1, 60))
        
        if duration != lastDuration:
            oled_update(str(duration))
        lastDuration = duration
        
    oled_update(str(duration) + " second timer.")
    sleep(3)
    
    
    