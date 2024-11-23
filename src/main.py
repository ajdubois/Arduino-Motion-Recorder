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
    
    
def oled_update(text):
    oled_clear()
    oled_print(text)
    
def signifyDataCollectionBegin():
    setLED(True)
    
def signifyDataCollectionEnd():
    setLED(False)
    
    

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
    if delay >= 5:
        oled_update("See console...")
        print("Data collection will begin when LED lights up...")
    


    sleep(delay)
    startTime = time()
    
    data_dictX = {}


    signifyDataCollectionBegin()
    while not isButtonPressed():
        sleep(sampleInterval)

        data_dictX[time() - startTime] = collectSampleAccelerationX() * 9.81 # in m/s

    signifyDataCollectionEnd()
    return data_dictX
    
    
# Delay is the delay before the start of data collection in seconds.
def collectDataWithTimer(delay, duration):
    if delay >= 5:
        oled_update("See console...")
        print("Data collection will begin when LED lights up...")
    
    
    sleep(delay)
    startTime = time()
    
    data_dictX = {}


    signifyDataCollectionBegin()
    while not time() >= startTime + duration:
        sleep(sampleInterval)

        data_dictX[time() - startTime] = collectSampleAccelerationX() * 9.81 # in m/s

    signifyDataCollectionEnd()
    return data_dictX
    
    
    
    
# Alloiw user to select a number between min and max using the dial, then return it
def dialNumberInput(min, max):
    selectedValue = math.floor(linearDialFunction(min, max))
    lastSelectedValue = selectedValue * -1 # Should not be the same at first

    while not isButtonPressed():
        sleep(0.15)
        selectedValue = math.floor(linearDialFunction(min, max))
        
        if selectedValue != lastSelectedValue:
            oled_update(str(selectedValue))
        lastSelectedValue = selectedValue
        
    return selectedValue




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

delay = dialNumberInput(1, 30)
    
        
oled_update(str(delay) + " second delay.")
sleep(3)


# get timer

oled_update("Timer duration...")
sleep(2.5)

acceleration = None # To be assigned in the following modes

if mode == "timer":
    duration = dialNumberInput(5, 60)
        
    oled_update(str(duration) + " second timer.")
    sleep(3)
    
    acceleration = collectDataWithTimer(delay, duration)
    
    
    
if mode == "button":
    acceleration = collectDataUntilButtonPress(delay)
    
    
    
# Graphing
oled_update("Data collection successful.")
sleep(2.5)

sampleCount = len(acceleration)

plt.plot(acceleration.keys(), acceleration.values())
plt.show()