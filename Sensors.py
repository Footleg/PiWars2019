#!/usr/bin/env python3

""" Mock sensor reading functions for PiWars Rocky Rover robot
"""
import random, time

#Sensors and channels configuration
leftDistance = 150
leftInc = 4
rightDistance = 180
rightInc = 1
frontDistance = 200
frontInc = 1
initialised = False
sensorsOn = False


def initialise():
    #Initialise sensors
    global initialised
    initialised = True

def startAll():
    global sensorsOn
    if initialised :
        sensorsOn = True
    else:
        raise RuntimeError("Sensors not initialised when calling startAll")
    
    
def stopAll():
    global sensorsOn
    if initialised :
        sensorsOn = False
    else:
        raise RuntimeError("Sensors not initialised when calling stopAll")
    
    
def readDistance(sensor):
    """ Read the distance from the specified tof sensor.
    """
    global leftDistance,rightDistance,frontDistance,leftInc,rightInc,frontInc
    
    if sensorsOn :
        minDist = 10
        maxDist = 300
        change = random.randint(2,10)
        flip = random.randint(1,20)
        
        if sensor == 1:
            #Left side sensor
            leftDistance = leftDistance + leftInc*change
            if (leftDistance > maxDist) or (leftDistance < minDist) or (flip==1):
                leftInc = -leftInc
                leftDistance = leftDistance + leftInc*change
            distance_in_mm = leftDistance
        elif sensor == 2:
            #Right side sensor
            rightDistance = rightDistance + rightInc*change
            if (rightDistance > maxDist) or (rightDistance < minDist) or (flip==1):
                rightInc = -rightInc
                rightDistance = rightDistance + rightInc*change
            distance_in_mm = rightDistance
        elif sensor == 3:
            #Front sensor
            frontDistance = frontDistance + frontInc*change
            if (frontDistance > maxDist) or (frontDistance < minDist) or (flip==1):
                frontInc = -frontInc
                frontDistance = frontDistance + frontInc*change
            distance_in_mm = frontDistance
        else:
            distance_in_mm = 0
            
        time.sleep(0.01)
        return distance_in_mm
    else:
        raise RuntimeError("Sensors not activated")


def test():
    """ Test sensors connected to multiplexer """
    initialise()
    startAll()
    for a in range(20):
        print("Left side distance: {}".format(readDistance(1)))
        print("Right side distance: {}".format(readDistance(2)))
        print("Front side distance: {}".format(readDistance(3)))
    stopAll()
    
    
if __name__ == '__main__':
    test()
