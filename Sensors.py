#!/usr/bin/env python3

""" Sensor reading functions for PiWars Rocky Rover robot
"""

from i2c_multiplexer import multiplexer
import VL53L1X, time

#Sensors and channels configuration
leftChannel = 7
rightChannel = 6
frontChannel = 5

#Initialise i2c multiplexer
plexer = multiplexer(1,0x70)

#Create sensor object (one instance does for all sensors)
tof1 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof2 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof3 = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tofs = [tof1,tof2,tof3]

def initialise():
    #Initialise sensors on all channels
    plexer.channel(leftChannel)
    tof1.open() # Initialise the i2c bus and configure the sensor
    plexer.channel(rightChannel)
    tof2.open() # Initialise the i2c bus and configure the sensor
    plexer.channel(frontChannel)
    tof3.open() # Initialise the i2c bus and configure the sensor


def getSensorChannel(sensor):
    if sensor == 1:
        #Left side sensor
        channel = leftChannel
    elif sensor == 2:
        #Right side sensor
        channel = rightChannel
    elif sensor == 3:
        #Right side sensor
        channel = frontChannel
    else:
        #Channel with no sensors
        channel = 0
        
    return channel


def start(sensor):
    """ Turn on a tof sensor.
    """
        
    #Activate sensor i2c channel
    plexer.channel( getSensorChannel(sensor) )
    
    #Open sensor to take reading
    tofs[sensor-1].start_ranging(1) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range


def startAll():
    for a in range(1,4):
        start(a)

def stop(sensor):
    """ Turn off a tof sensor.
    """
        
    #Activate sensor i2c channel
    plexer.channel( getSensorChannel(sensor) )
    
    #Open sensor to take reading
    tofs[sensor-1].stop_ranging() # Stop ranging
    

def stopAll():
    for a in range(1,4):
        start(a)

def readDistance(sensor):
    """ Read the distance from the specified tof sensor.
    """
        
    #Activate sensor i2c channel
    plexer.channel( getSensorChannel(sensor) )
    
    distance_in_mm = tofs[sensor-1].get_distance() # Grab the range in mm

    return distance_in_mm


def test():
    """ Test sensors connected to multiplexer """
    initialise()
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
