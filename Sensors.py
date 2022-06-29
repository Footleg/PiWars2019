#!/usr/bin/env python3

""" Sensor reading functions for PiWars Rocky Rover robot
"""

import time
import board
import digitalio
import adafruit_vl53l1x

#Sensors and channels configuration
leftSensorAddr = 0x30
rightSensorAddr = 0x31
frontSensorAddr = 0x29
leftSensorEnableIO = 0
rightSensorEnableIO = 1
frontSensorEnableIO = 2

i2c = board.I2C()

tof1 = 0
tof2 = 0
tof3 = adafruit_vl53l1x.VL53L1X(i2c)
tof3.distance_mode = 1
tof3.timing_budget = 100

tofs = [tof1,tof2,tof3]


def start(sensor):
    """ Turn on a tof sensor.
    """
    try:    
        #Open sensor to take reading
        tofs[sensor-1].start_ranging()
    except:
        print(f"Error starting sensor {sensor}")

def startAll():
    for a in range(3,4):
        start(a)

def stop(sensor):
    """ Turn off a tof sensor.
    """
    
    try:    
        tofs[sensor-1].stop_ranging() # Stop ranging
    except:
        print(f"Error stoping sensor {sensor}")
    
    

def stopAll():
    for a in range(3,4):
        stop(a)

def readDistance(sensor):
    """ Read the distance from the specified tof sensor.
    """
    if sensor < 3:
        distance_in_mm = 10
    else:
        # Try 3 times to get a reading
        vl53 = tofs[sensor-1]
        distance_in_mm = 0
        for a in range(3):
            if vl53.data_ready:
                 distance_in_mm = vl53.distance * 10 # Sensor library returns cm as float
                 vl53.clear_interrupt()
            if distance_in_mm > 0:
                break
            else:
                time.sleep(0.1)

    return distance_in_mm


def test():
    """ Test sensors connected to multiplexer """
    for a in range(1,4):
        start(a)
        time.sleep(0.1)
    for b in range(5):   
        timeC = time.perf_counter()
        print("Left side distance: {}".format(readDistance(1)))
        print("Right side distance: {}".format(readDistance(2)))
        print("Front distance: {}".format(readDistance(3)))
        print("Sensor Read time: {:.2f}".format( time.perf_counter() - timeC ) )
    for a in range(1,4):
        stop(a)
    
    
if __name__ == '__main__':
    test()
