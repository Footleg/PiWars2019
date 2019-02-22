#!/usr/bin/env python3

""" Sensor reading functions for PiWars Rocky Rover robot
"""

from i2c_multiplexer import multiplexer
import VL53L1X

#Sensors and channels configuration
leftChannel = 7
rightChannel = 6

#Initialise i2c multiplexer
plexer = multiplexer(1,0x70)

#Create sensor object (one instance does for all sensors)
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)

#Initialise sensors on all channels
plexer.channel(leftChannel)
tof.open() # Initialise the i2c bus and configure the sensor
plexer.channel(rightChannel)
tof.open() # Initialise the i2c bus and configure the sensor


def readDistance(sensor):
    """ Read the distance from the specified tof sensor.
    """
    if sensor == 1:
        #Left side sensor
        channel = leftChannel
    elif sensor == 2:
        #Right side sensor
        channel = rightChannel
        
    #Activate sensor i2c channel
    plexer.channel(channel)
    
    #Open sensor to take reading
#    tof.open() # Initialise the i2c bus and configure the sensor
    tof.start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range
    distance_in_mm = tof.get_distance() # Grab the range in mm
    tof.stop_ranging() # Stop ranging

    return distance_in_mm


def test():
    """ Test sensors connected to multiplexer """
    print("Left side distance: {}".format(readDistance(1)))
    print("Right side distance: {}".format(readDistance(2)))
    
if __name__ == '__main__':
    test()
