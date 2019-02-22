#!/usr/bin/env python3

""" Mock sensor reading functions for PiWars Rocky Rover robot
"""
import random

#Sensors and channels configuration
leftDistance = 100
leftInc = 10
rightDistance = 100
rightInc = 10


def readDistance(sensor):
    """ Read the distance from the specified tof sensor.
    """
    global leftDistance,rightDistance,leftInc,rightInc
    
    change = random.randint(5,25) 
    
    if sensor == 1:
        #Left side sensor
        leftInc = leftInc + change
        leftDistance = leftDistance + leftInc
        if leftDistance > 500:
            leftDistance = leftDistance - leftInc
            leftInc = -change
        elif leftDistance < 10:
            leftDistance = leftDistance - leftInc
            leftInc = change
        distance_in_mm = leftDistance
    elif sensor == 2:
        #Right side sensor
        rightInc = rightInc + change
        rightDistance = rightDistance + rightInc
        if rightDistance > 500:
            rightDistance = rightDistance - rightInc
            rightInc = -change
        elif rightDistance < 10:
            rightDistance = rightDistance - rightInc
            rightInc = change
        distance_in_mm = rightDistance

    return distance_in_mm


def test():
    """ Test sensors connected to multiplexer """
    print("Left side distance: {}".format(readDistance(1)))
    print("Right side distance: {}".format(readDistance(2)))
    
if __name__ == '__main__':
    test()
