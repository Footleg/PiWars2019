#!/usr/bin/env python3

""" Mock sensor reading functions for PiWars Rocky Rover robot
"""
import random

#Sensors and channels configuration
leftDistance = 100
leftInc = 1
rightDistance = 100
rightInc = 1
frontDistance = 100
frontInc = 1


def readDistance(sensor):
    """ Read the distance from the specified tof sensor.
    """
    global leftDistance,rightDistance,frontDistance,leftInc,rightInc,frontInc
    
    minDist = 10
    maxDist = 2000
    change = random.randint(5,25)
    
    if sensor == 1:
        #Left side sensor
        leftDistance = leftDistance + leftInc*change
        if (leftDistance > maxDist) or (leftDistance < minDist):
            leftInc = -leftInc
            leftDistance = leftDistance + leftInc*change
        distance_in_mm = leftDistance
    elif sensor == 2:
        #Right side sensor
        rightDistance = rightDistance + rightInc*change
        if (rightDistance > maxDist) or (rightDistance < minDist):
            rightInc = -rightInc
            rightDistance = rightDistance + rightInc*change
        distance_in_mm = rightDistance
    elif sensor == 3:
        #Front sensor
        frontDistance = frontDistance + frontInc*change
        if (frontDistance > maxDist) or (frontDistance < minDist):
            frontInc = -frontInc
            frontDistance = frontDistance + frontInc*change
        distance_in_mm = frontDistance
    else:
        distance_in_mm = 0
        
    return distance_in_mm


def test():
    """ Test sensors connected to multiplexer """
    for a in range(20):
        print("Left side distance: {}".format(readDistance(1)))
        print("Right side distance: {}".format(readDistance(2)))
        print("Front side distance: {}".format(readDistance(3)))
    
if __name__ == '__main__':
    test()
