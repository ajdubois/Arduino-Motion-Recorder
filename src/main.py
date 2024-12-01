import math
from time import sleep
from time import time
from engi1020.arduino.api import *
from engi1020.arduino.pressure import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
from datacollect import *
from graph import *
from inout import *




axisText = input("Which axis would you like to record? ").lower()

xAxisEnabled = bool(re.search(r"x", axisText))
if xAxisEnabled:
    print("X axis enabled.")

yAxisEnabled = bool(re.search(r"y", axisText))
if yAxisEnabled:
    print("Y axis enabled.")
zAxisEnabled = bool(re.search(r"z", axisText))
if zAxisEnabled:
    print("Z axis enabled.")
    
    
accelerationEnabled = bool(re.search(r"a", axisText))

velocityEnabled = bool(re.search(r"v", axisText))

positionEnabled = bool(re.search(r"p", axisText))

if not accelerationEnabled and not velocityEnabled and not positionEnabled: # defaults
    accelerationEnabled = True
    velocityEnabled = True
    

if not accelerationEnabled:
    print("Acceleration disabled.")
if not velocityEnabled:
    print("Velocity disabled.")
if positionEnabled:
    print("Position enabled.")
    
    
    
    
    
oled_update("Calibrating...") # This is important for registering the arduino before calibration,it is not just to look cool.
    

# calibration

print("keep the arduino still while it calibrates.")

zeroTime = 10

print("This will take " + str(zeroTime) + " seconds.")


startTime = time()

xSampleSum = 0
ySampleSum = 0
zSampleSum = 0

sampleCount = 0

print("\nCalibrating...")
signifyDataCollectionBegin()
while time() - startTime < zeroTime:
    xSampleSum = xSampleSum + collectSampleAccelerationX()
    ySampleSum = ySampleSum + collectSampleAccelerationY()
    zSampleSum = zSampleSum + collectSampleAccelerationZ()
    sampleCount = sampleCount + 1
    
    
 

signifyDataCollectionEnd()
xZero = xSampleSum / sampleCount
yZero = ySampleSum / sampleCount
zZero = zSampleSum / sampleCount


print("Calibration complete. See OLED for instructions.")





sampleInterval = 0.01 # Interval in seconds between sample collection.


    
    


def delayForSeconds(seconds):
    if delay > 0:
        oled_update(str(seconds) + "s delay...")
        sleep(seconds)
    else:
        oled_update("No delay; starting.")


# Set mode


mode = "timer" # can be "timer" or "button".


oled_update("Select mode.")
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
sleep(2)

delay = dialNumberInput(0, 15)
    
        
delayForSeconds(delay)
    
    
    
    
    

accelerationX = None # To be assigned in the following modes
accelerationY = None # To be assigned in the following modes
accelerationZ = None # To be assigned in the following modes

if mode == "timer":
    oled_update("Timer duration...")
    sleep(2.5)

    duration = dialNumberInput(5, 40)
        
    oled_update(str(duration) + " second timer.")
    sleep(3)
    
    accelerationX, accelerationY, accelerationZ = collectDataWithTimer(duration, xZero, yZero, zZero)
    
    
    
if mode == "button":
    #accelerations = collectDataUntilButtonPress()
    #accelerationX = accelerations[0]
    #accelerationY = accelerations[1]
    #accelerationZ = accelerations[2]
    
    accelerationX, accelerationY, accelerationZ = collectDataUntilButtonPress(xZero, yZero, zZero)
    
    



    
# Graphing
oled_update("Data collection successful.")
sleep(2.5)





if not xAxisEnabled:
    accelerationX = None
if not yAxisEnabled:
    accelerationY = None
if not zAxisEnabled:
    accelerationZ = None
    

drawGraphs(accelerationX, accelerationY, accelerationZ, accelerationEnabled, velocityEnabled, positionEnabled)