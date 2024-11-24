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
    
def setBuzzer(num):
    analog_write(2, num)
    
def signifyDataCollectionBegin():
    setLED(True)
    setBuzzer(255)
    
def signifyDataCollectionEnd():
    setLED(False)
    setBuzzer(0)
    
    

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


oled_update("Select desired mode.")
sleep(4)

if getRotaryDialValue() > maxAnalogValue / 2:
    mode = "timer"
else:
    mode = "button"

oled_update(mode)
lastMode = mode

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



acceleration = None # To be assigned in the following modes

if mode == "timer":
    oled_update("Timer duration...")
    sleep(2.5)

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

# acceleration
plt.subplot(131)
plt.plot(acceleration.keys(), acceleration.values(), "r-")
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s/s)')



# velocity


# return integral of the provided dictionary
def integral(dictionary):
    lastKey = None
    lastValue = None
    
    samplesProcessed = 0
    
    integral = {}
    
    
    for key in dictionary.keys():
        value = dictionary[key]
        if samplesProcessed != 0:
            rectangleArea = lastValue * (key - lastKey)
            triangleArea = (value - lastValue) * (key - lastKey) * 0.5
            
            index = (key + lastKey) * 0.5
            
            integral[index] = rectangleArea + triangleArea
            
        samplesProcessed = samplesProcessed + 1
        lastKey = key
        lastValue = value
        
    return integral


velocity = integral(acceleration)
    


plt.subplot(132)
plt.plot(velocity.keys(), velocity.values(), "g-")
plt.xlabel('Time (s)')
plt.ylabel('Change in Velocity Due to Acceleration (m/s)')

plt.title("Motion from acceleration (" + str(sampleCount) + " samples)")



position = integral(velocity)
    


plt.subplot(133)
plt.plot(position.keys(), position.values(), "b-")
plt.xlabel('Time (s)')
plt.ylabel('Change in Position Due to Acceleration (m)')



plt.show()