from engi1020.arduino.api import *
from time import sleep
from time import time
import math


maxAnalogValue = 1023


def setLED(activated):
    digital_write(4, activated)
    
    
def oled_update(text):
    oled_clear()
    oled_print(text)
    



def isButtonPressed():
    return digital_read(6)
    

def getRotaryDialValue():
    return analog_read(0)

def linearDialFunction(min, max):
    dialValue = getRotaryDialValue()
    slope = (max - min) / maxAnalogValue
    return slope * dialValue + min
    
    
    

# Alloiw user to select a number between min and max using the dial, then return it
def dialNumberInput(min, max):
    selectedValue = math.floor(linearDialFunction(min, max))
    lastSelectedValue = math.pi # arbitrary number

    while not isButtonPressed():
        sleep(0.15)
        selectedValue = math.floor(linearDialFunction(min, max))
        
        if selectedValue != lastSelectedValue:
            oled_update(str(selectedValue))
        lastSelectedValue = selectedValue
        
    return selectedValue