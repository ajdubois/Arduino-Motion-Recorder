import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd





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
                
                area = rectangleArea + triangleArea
                
                if sign(area) != sign(value):
                    area = area * -1
                
                areaSum = areaSum + area
            
                integral[key] = areaSum
            else:
                xIntercept = -1 * lastValue*(key-lastKey)/(value-lastValue) + lastKey
                
                xInterceptScaled = xIntercept - lastKey
                
                totalWidth = key - lastKey
                secondTriangleWidth = totalWidth - xInterceptScaled
                firstTriangleWidth = totalWidth - secondTriangleWidth
            
                areaFirstTriangle = firstTriangleWidth*lastValue/2
                areaSecondTriangle = secondTriangleWidth*value/2
                
                areaSum = areaSum + areaFirstTriangle + areaSecondTriangle
                
                integral[key] = areaSum
        else:
            integral[key] = 0
            
            
        samplesProcessed = samplesProcessed + 1
        lastKey = key
        lastValue = value
        
    return integral
    
    
    
    
    
   
def drawGraphs(xAccel=None, yAccel=None, zAccel=None, accelerationEnabled=True, velocityEnabled=True, positionEnabled=False):
    velocityX = None
    velocityY = None
    velocityZ = None
                
    positionX = None
    positionY = None
    positionZ = None


    axisGroups = 0

    if xAccel:
        axisGroups = axisGroups + 1
        velocityX = integral(xAccel)
        positionX = integral(velocityX)
        
    if yAccel:
        axisGroups = axisGroups + 1
        velocityY = integral(yAccel)
        positionY = integral(velocityY)
        
    if zAccel:
        axisGroups = axisGroups + 1
        velocityZ = integral(zAccel)
        positionZ = integral(velocityZ)
        
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
        if xAccel:
            if accelerationEnabled:
                ax[rowsUsed, 0].plot(list(xAccel.keys()), list(xAccel.values()), "r-")
                ax[rowsUsed, 0].set_xlabel("Time (s)")
                ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
            if velocityEnabled:
                ax[rowsUsed, 1].plot(list(velocityX.keys()), list(velocityX.values()), "g-")
                ax[rowsUsed, 1].set_xlabel("Time (s)")
                ax[rowsUsed, 1].set_ylabel("Velocity from acceleration (m/s)")
                ax[rowsUsed, 1].set_title("X axis")
            if positionEnabled:
                ax[rowsUsed, 2].plot(list(positionX.keys()), list(positionX.values()), "b-")
                ax[rowsUsed, 2].set_xlabel("Time (s)")
                ax[rowsUsed, 2].set_ylabel("Position from acceleration (m)")
            
            rowsUsed = rowsUsed + 1
            
        if yAccel:
            if accelerationEnabled:
                ax[rowsUsed, 0].plot(list(yAccel.keys()), list(yAccel.values()), "r-")
                ax[rowsUsed, 0].set_xlabel("Time (s)")
                ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
            if velocityEnabled:
                ax[rowsUsed, 1].plot(list(velocityY.keys()), list(velocityY.values()), "g-")
                ax[rowsUsed, 1].set_xlabel("Time (s)")
                ax[rowsUsed, 1].set_ylabel("Velocity from acceleration (m/s)")
                ax[rowsUsed, 1].set_title("Y axis")
            if positionEnabled:
                ax[rowsUsed, 2].plot(list(positionY.keys()), list(positionY.values()), "b-")
                ax[rowsUsed, 2].set_xlabel("Time (s)")
                ax[rowsUsed, 2].set_ylabel("Position from acceleration (m)")
            
            rowsUsed = rowsUsed + 1
            
        if zAccel:
            if accelerationEnabled:
                ax[rowsUsed, 0].plot(list(zAccel.keys()), list(zAccel.values()), "r-")
                ax[rowsUsed, 0].set_xlabel("Time (s)")
                ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
            if velocityEnabled:
                ax[rowsUsed, 1].plot(list(velocityZ.keys()), list(velocityZ.values()), "g-")
                ax[rowsUsed, 1].set_xlabel("Time (s)")
                ax[rowsUsed, 1].set_ylabel("Velocity from acceleration (m/s)")
                ax[rowsUsed, 1].set_title("Z axis")
            if positionEnabled:
                ax[rowsUsed, 2].plot(list(positionZ.keys()), list(positionZ.values()), "b-")
                ax[rowsUsed, 2].set_xlabel("Time (s)")
                ax[rowsUsed, 2].set_ylabel("Position from acceleration (m)")
            
            rowsUsed = rowsUsed + 1
            
    else:
        if xAccel:
            if accelerationEnabled:
                ax[0].plot(list(xAccel.keys()), list(xAccel.values()), "r-")
                ax[0].set_xlabel("Time (s)")
                ax[0].set_ylabel("Acceleration (m/s/s)")
            if velocityEnabled:
                ax[1].plot(list(velocityX.keys()), list(velocityX.values()), "g-")
                ax[1].set_xlabel("Time (s)")
                ax[1].set_ylabel("Velocity from acceleration (m/s)")
            if positionEnabled:
                ax[2].plot(list(positionX.keys()), list(positionX.values()), "b-")
                ax[2].set_xlabel("Time (s)")
                ax[2].set_ylabel("Position from acceleration (m)")
            
        if yAccel:
            if accelerationEnabled:
                ax[0].plot(list(yAccel.keys()), list(yAccel.values()), "r-")
                ax[0].set_xlabel("Time (s)")
                ax[0].set_ylabel("Acceleration (m/s/s)")
            if velocityEnabled:
                ax[1].plot(list(velocityY.keys()), list(velocityY.values()), "g-")
                ax[1].set_xlabel("Time (s)")
                ax[1].set_ylabel("Velocity from acceleration (m/s)")
            if positionEnabled:
                ax[2].plot(list(positionY.keys()), list(positionY.values()), "b-")
                ax[2].set_xlabel("Time (s)")
                ax[2].set_ylabel("Position from acceleration (m)")
            
        if zAccel:
            if accelerationEnabled:
                ax[0].plot(list(zAccel.keys()), list(zAccel.values()), "r-")
                ax[0].set_xlabel("Time (s)")
                ax[0].set_ylabel("Acceleration (m/s/s)")
            if velocityEnabled:
                ax[1].plot(list(velocityZ.keys()), list(velocityZ.values()), "g-")
                ax[1].set_xlabel("Time (s)")
                ax[1].set_ylabel("Velocity from acceleration (m/s)")
            if positionEnabled:
                ax[2].plot(list(positionZ.keys()), list(positionZ.values()), "b-")
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
    
        if xAccel:
            absoluteAcceleration = xAccel.copy()
            if yAccel:
                absoluteAcceleration = pythagoreanMerge(absoluteAcceleration, yAccel)
            if zAccel:
                absoluteAcceleration = pythagoreanMerge(absoluteAcceleration, zAccel)
                
        elif yAccel:
            absoluteAcceleration = yAccel.copy()
            if zAccel:
                absoluteAcceleration = pythagoreanMerge(absoluteAcceleration, zAccel)
        
        else:
            absoluteAcceleration = zAccel.copy()
            
            
        absoluteVelocity = integral(absoluteAcceleration)
        absolutePosition = integral(absoluteVelocity)
        
        
        if accelerationEnabled:
            ax[rowsUsed, 0].plot(list(absoluteAcceleration.keys()), list(absoluteAcceleration.values()), "r-")
            ax[rowsUsed, 0].set_xlabel("Time (s)")
            ax[rowsUsed, 0].set_ylabel("Acceleration (m/s/s)")
        
        if velocityEnabled:
            ax[rowsUsed, 1].plot(list(absoluteVelocity.keys()), list(absoluteVelocity.values()), "g-")
            ax[rowsUsed, 1].set_xlabel("Time (s)")
            ax[rowsUsed, 1].set_ylabel("Velocity (m/s)")
        ax[rowsUsed, 1].set_title("Magnitudinal")
        
        if positionEnabled:
            ax[rowsUsed, 2].plot(list(absolutePosition.keys()), list(absolutePosition.values()), "b-")
            ax[rowsUsed, 2].set_xlabel("Time (s)")
            ax[rowsUsed, 2].set_ylabel("Distance (m)")
        
        rowsUsed = rowsUsed + 1
    
    
    
    
    plt.show()