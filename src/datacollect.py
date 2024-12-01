from inout import *
from time import sleep
from time import time



def collectSampleAccelerationX(zero=0):
    return three_axis_get_accelX() - zero
    
def collectSampleAccelerationY(zero=0):
    return three_axis_get_accelY() - zero
    
def collectSampleAccelerationZ(zero=0):
    return three_axis_get_accelZ() - zero
    
    
    
def signifyDataCollectionBegin():
    setLED(True)
    
def signifyDataCollectionEnd():
    setLED(False)
    
    
    
    
    
# Delay is the delay before the start of data collection in seconds.
def collectDataUntilButtonPress(xZero, yZero, zZero):
    startTime = time()
    
    data_dictX = {}
    data_dictY = {}
    data_dictZ = {}


    signifyDataCollectionBegin()
    while not isButtonPressed():

        data_dictX[time() - startTime] = collectSampleAccelerationX(xZero) * 9.81 # in m/s
        data_dictY[time() - startTime] = collectSampleAccelerationY(yZero) * 9.81 # in m/s
        data_dictZ[time() - startTime] = collectSampleAccelerationZ(zZero) * 9.81 # in m/s

    signifyDataCollectionEnd()
    return [data_dictX, data_dictY, data_dictZ]
    
    
# Delay is the delay before the start of data collection in seconds.
def collectDataWithTimer(duration, xZero, yZero, zZero):
    startTime = time()
    
    data_dictX = {}
    data_dictY = {}
    data_dictZ = {}


    signifyDataCollectionBegin()
    while not time() >= startTime + duration:

        data_dictX[time() - startTime] = collectSampleAccelerationX(xZero) * 9.81 # in m/s
        data_dictY[time() - startTime] = collectSampleAccelerationY(yZero) * 9.81 # in m/s
        data_dictZ[time() - startTime] = collectSampleAccelerationZ(zZero) * 9.81 # in m/s

    signifyDataCollectionEnd()
    return [data_dictX, data_dictY, data_dictZ]