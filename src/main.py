import math
from time import sleep
from time import time
from engi1020.arduino.api import *
from engi1020.arduino.pressure import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re


maxAnalogValue = 1023



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
    
    
    
oled_update("Calibrating...") # This is important for registering the arduino before calibration,it is not just to look cool.
    

# calibration

print("keep the arduino still while it calibrates.")

zeroTime = 3.5  

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


def collectSampleAccelerationX():
    return three_axis_get_accelX()# - xZero
    
def collectSampleAccelerationY():
    return three_axis_get_accelY()# - yZero
    
def collectSampleAccelerationZ():
    return three_axis_get_accelZ() - zZero


print("Calibration complete.")



    

def isButtonPressed():
    return digital_read(6)
    

def getRotaryDialValue():
    return analog_read(0)

def linearDialFunction(min, max):
    dialValue = getRotaryDialValue()
    slope = (max - min) / maxAnalogValue
    return slope * dialValue + min



sampleInterval = 0.01 # Interval in seconds between sample collection.



# Delay is the delay before the start of data collection in seconds.
def collectDataUntilButtonPress():
    startTime = time()
    
    data_dictX = {}
    data_dictY = {}
    data_dictZ = {}


    signifyDataCollectionBegin()
    while not isButtonPressed():

        data_dictX[time() - startTime] = collectSampleAccelerationX() * 9.81 # in m/s
        data_dictY[time() - startTime] = collectSampleAccelerationY() * 9.81 # in m/s
        data_dictZ[time() - startTime] = collectSampleAccelerationZ() * 9.81 # in m/s

    signifyDataCollectionEnd()
    return [data_dictX, data_dictY, data_dictZ]
    
    
# Delay is the delay before the start of data collection in seconds.
def collectDataWithTimer(duration):
    startTime = time()
    
    data_dictX = {}
    data_dictY = {}
    data_dictZ = {}


    signifyDataCollectionBegin()
    while not time() >= startTime + duration:

        data_dictX[time() - startTime] = collectSampleAccelerationX() * 9.81 # in m/s
        data_dictY[time() - startTime] = collectSampleAccelerationY() * 9.81 # in m/s
        data_dictZ[time() - startTime] = collectSampleAccelerationZ() * 9.81 # in m/s

    signifyDataCollectionEnd()
    return [data_dictX, data_dictY, data_dictZ]
    
    
    
    
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


def delayForSeconds(seconds):
    if delay > 0:
        oled_update(str(seconds) + "s delay...")
        sleep(seconds)
    else:
        oled_update("No delay; starting.")
        sleep(1.5)


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







def sign(num):
    return math.copysign(1, num)

# return integral of the provided dictionary
def integral(dictionary):
    lastKey = None
    lastValue = None
    
    samplesProcessed = 0
    
    areaSum = 0
    
    integral = {}
    
    
    for key in dictionary.keys():
        value = dictionary[key]
        if samplesProcessed != 0:
            if sign(value) == sign(lastValue):
                rectangleArea = lastValue * (key - lastKey)
                triangleArea = (value - lastValue) * (key - lastKey) * 0.5
            
                index = (key + lastKey) * 0.5
                
                areaSum = areaSum + rectangleArea + triangleArea
            
                integral[index] = areaSum
            else:
                area = (key - lastKey)*(value + lastValue)/4
            
                index = (key + lastKey) * 0.5
                
                areaSum = areaSum + area
                
                integral[index] = areaSum
            
            
        samplesProcessed = samplesProcessed + 1
        lastKey = key
        lastValue = value
        
    return integral
    
    
    
    
    

accelerationX = None # To be assigned in the following modes
accelerationY = None # To be assigned in the following modes
accelerationZ = None # To be assigned in the following modes

if mode == "timer":
    oled_update("Timer duration...")
    sleep(2.5)

    duration = dialNumberInput(5, 60)
        
    oled_update(str(duration) + " second timer.")
    sleep(3)
    
    accelerations = collectDataWithTimer(duration)
    accelerationX = accelerations[0]
    accelerationY = accelerations[1]
    accelerationZ = accelerations[2]
    
    accelerationX, accelerationY, accelerationZ = collectDataWithTimer(duration)
    
    
    
if mode == "button":
    accelerations = collectDataUntilButtonPress()
    accelerationX = accelerations[0]
    accelerationY = accelerations[1]
    accelerationZ = accelerations[2]
    


# intergration

velocityX = integral(accelerationX)
velocityY = integral(accelerationY)
velocityZ = integral(accelerationZ)

positionX = integral(velocityX)
positionY = integral(velocityY)
positionZ = integral(velocityZ)



    
# Graphing
oled_update("Data collection successful.")
sleep(2.5)



axisGroups = 0

if xAxisEnabled:
    axisGroups = axisGroups + 1
if yAxisEnabled:
    axisGroups = axisGroups + 1
if zAxisEnabled:
    axisGroups = axisGroups + 1
if axisGroups > 1:
    axisGroups = axisGroups + 1 # absolute motion
    
    
fig = None
ax = None
if positionEnabled:
    fig, ax = plt.subplots(axisGroups, 3)
else:
    fig, ax = plt.subplots(axisGroups, 2)



rowsUsed = 0


if axisGroups > 1:
    if xAxisEnabled:
        if accelerationEnabled:
            ax[rowsUsed, 0].plot(accelerationX.keys(), accelerationX.values(), "r-")
            ax[rowsUsed, 0].set_xlabel("Time (s)")
            ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
        if velocityEnabled:
            ax[rowsUsed, 1].plot(velocityX.keys(), velocityX.values(), "g-")
            ax[rowsUsed, 1].set_xlabel("Time (s)")
            ax[rowsUsed, 1].set_ylabel("Velocity from acceleration (m/s)")
            ax[rowsUsed, 1].set_title("X axis")
        if positionEnabled:
            ax[rowsUsed, 2].plot(positionX.keys(), positionX.values(), "b-")
            ax[rowsUsed, 2].set_xlabel("Time (s)")
            ax[rowsUsed, 2].set_ylabel("Position from acceleration (m)")
        
        rowsUsed = rowsUsed + 1
        
    if yAxisEnabled:
        if accelerationEnabled:
            ax[rowsUsed, 0].plot(accelerationY.keys(), accelerationY.values(), "r-")
            ax[rowsUsed, 0].set_xlabel("Time (s)")
            ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
        if velocityEnabled:
            ax[rowsUsed, 1].plot(velocityY.keys(), velocityY.values(), "g-")
            ax[rowsUsed, 1].set_xlabel("Time (s)")
            ax[rowsUsed, 1].set_ylabel("Velocity from acceleration (m/s)")
            ax[rowsUsed, 1].set_title("Y axis")
        if positionEnabled:
            ax[rowsUsed, 2].plot(positionY.keys(), positionY.values(), "b-")
            ax[rowsUsed, 2].set_xlabel("Time (s)")
            ax[rowsUsed, 2].set_ylabel("Position from acceleration (m)")
        
        rowsUsed = rowsUsed + 1
        
    if zAxisEnabled:
        if accelerationEnabled:
            ax[rowsUsed, 0].plot(accelerationZ.keys(), accelerationZ.values(), "r-")
            ax[rowsUsed, 0].set_xlabel("Time (s)")
            ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
        if velocityEnabled:
            ax[rowsUsed, 1].plot(velocityZ.keys(), velocityZ.values(), "g-")
            ax[rowsUsed, 1].set_xlabel("Time (s)")
            ax[rowsUsed, 1].set_ylabel("Velocity from acceleration (m/s)")
            ax[rowsUsed, 1].set_title("Z axis")
        if positionEnabled:
            ax[rowsUsed, 2].plot(positionZ.keys(), positionZ.values(), "b-")
            ax[rowsUsed, 2].set_xlabel("Time (s)")
            ax[rowsUsed, 2].set_ylabel("Position from acceleration (m)")
        
        rowsUsed = rowsUsed + 1
        
else:
    if xAxisEnabled:
        if accelerationEnabled:
            ax[0].plot(accelerationX.keys(), accelerationX.values(), "r-")
            ax[0].set_xlabel("Time (s)")
            ax[0].set_ylabel("Acceleration (m/s/s)")
        if velocityEnabled:
            ax[1].plot(velocityX.keys(), velocityX.values(), "g-")
            ax[1].set_xlabel("Time (s)")
            ax[1].set_ylabel("Velocity from acceleration (m/s)")
        if positionEnabled:
            ax[2].plot(positionX.keys(), positionX.values(), "b-")
            ax[2].set_xlabel("Time (s)")
            ax[2].set_ylabel("Position from acceleration (m)")
        
    if yAxisEnabled:
        if accelerationEnabled:
            ax[0].plot(accelerationY.keys(), accelerationY.values(), "r-")
            ax[0].set_xlabel("Time (s)")
            ax[0].set_ylabel("Acceleration (m/s/s)")
        if velocityEnabled:
            ax[1].plot(velocityY.keys(), velocityY.values(), "g-")
            ax[1].set_xlabel("Time (s)")
            ax[1].set_ylabel("Velocity from acceleration (m/s)")
        if positionEnabled:
            ax[2].plot(positionY.keys(), positionY.values(), "b-")
            ax[2].set_xlabel("Time (s)")
            ax[2].set_ylabel("Position from acceleration (m)")
        
    if zAxisEnabled:
        if accelerationEnabled:
            ax[0].plot(accelerationZ.keys(), accelerationZ.values(), "r-")
            ax[0].set_xlabel("Time (s)")
            ax[0].set_ylabel("Acceleration (m/s/s)")
        if velocityEnabled:
            ax[1].plot(velocityZ.keys(), velocityZ.values(), "g-")
            ax[1].set_xlabel("Time (s)")
            ax[1].set_ylabel("Velocity from acceleration (m/s)")
        if positionEnabled:
            ax[2].plot(positionZ.keys(), positionZ.values(), "b-")
            ax[2].set_xlabel("Time (s)")
            ax[2].set_ylabel("Position from acceleration (m)")
    

def closestKey(key, dict):
    closest = None
    
    for k in dict.keys():
        if closest == None:
            closest = k
        else:
            if abs(closest - key) > abs(k - key):
                closest = k
                
    return closest
    
    
    

    
def pythagoreanMerge(dict1, dict2):
    dict3 = dict1.copy()
    
    for k in dict3.keys():
        v = dict3[k]
        ov = dict2[closestKey(k, dict2)]
        
        nv = math.sqrt(v**2 + ov**2)
        dict3[k] = nv
        
    return dict3
        
        

absoluteAcceleration = None
if axisGroups > 1:

    if xAxisEnabled:
        absoluteAcceleration = accelerationX.copy()
        if yAxisEnabled:
            absoluteAcceleration = pythagoreanMerge(absoluteAcceleration, accelerationY)
        if zAxisEnabled:
            absoluteAcceleration = pythagoreanMerge(absoluteAcceleration, accelerationZ)
            
    elif yAxisEnabled:
        absoluteAcceleration = accelerationY.copy()
        if zAxisEnabled:
            absoluteAcceleration = pythagoreanMerge(absoluteAcceleration, accelerationZ)
    
    else:
        absoluteAcceleration = accelerationZ.copy()
        
        
    absoluteVelocity = integral(absoluteAcceleration)
    absolutePosition = integral(absoluteVelocity)
    
    
    
    ax[rowsUsed, 0].plot(absoluteAcceleration.keys(), absoluteAcceleration.values(), "r-")
    ax[rowsUsed, 0].set_xlabel("Time (s)")
    ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
    
    ax[rowsUsed, 1].plot(absoluteVelocity.keys(), absoluteVelocity.values(), "g-")
    ax[rowsUsed, 1].set_xlabel("Time (s)")
    ax[rowsUsed, 1].set_ylabel("Velocity (m/s)")
    ax[rowsUsed, 1].set_title("Magnitudinal")
    
    if positionEnabled:
        ax[rowsUsed, 2].plot(absolutePosition.keys(), absolutePosition.values(), "b-")
        ax[rowsUsed, 2].set_xlabel("Time (s)")
        ax[rowsUsed, 2].set_ylabel("Distance (m)")
    
    rowsUsed = rowsUsed + 1
    
            





sampleCount = len(accelerationX)




plt.show()