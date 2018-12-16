#!/usr/bin/python

""" PiWars Rocky Rover robot control functions module
"""

import AdafruitPWMboard as pwmb

#Servo calibration and configuration constants
servoFrontLeftOffset = 14
servoFrontRightOffset = 36
servoRearLeftOffset = 16
servoRearRightOffset = 24

servoFrontLeftChannel = 4
servoFrontRightChannel = 5
servoRearLeftChannel = 6
servoRearRightChannel = 7

servoMinAngle = 40
servoMaxAngle = 180

#==========================================================================================
# Safe steering functions to ensure servos are not set beyond their limits of free movement
#==========================================================================================
def setSteeringLegPositionSafely(angle, servoChannel, servoOffset):
    """ Sets the position of the front left steering servo. Does not allow the servo to 
        be set to a postion beyond the range of free movement of the steering leg
    """
    #Correct servo position if set beyond safe range
    if (angle < servoMinAngle): 
        servoPos = servoMinAngle
    elif (angle > servoMaxAngle): 
        servoPos = servoMaxAngle
    else:
        servoPos = angle
        
    #Adjust servo position with offset so 90 degrees is when wheel is pointing straight ahead
    servoPos = servoPos + servoOffset
    
    #Set servo position
    pwmb.setServoPosition(servoChannel, servoPos) 
    
def setSteeringFrontLeft(angle):
    """ Sets the position of the front left steering servo """
    setSteeringLegPositionSafely(angle, servoFrontLeftChannel, servoFrontLeftOffset)
    
def setSteeringFrontRight(angle):
    """ Sets the position of the front right steering servo """
    setSteeringLegPositionSafely(angle, servoFrontRightChannel, servoFrontRightOffset)
    
def setSteeringRearLeft(angle):
    """ Sets the position of the rear left steering servo """
    setSteeringLegPositionSafely(angle, servoRearLeftChannel, servoRearLeftOffset)
    
def setSteeringRearRight(angle):
    """ Sets the position of the rear right steering servo """
    setSteeringLegPositionSafely(angle, servoRearRightChannel, servoRearRightOffset)
    
    
def spotTurnSteering(angle):
    """ Turns all wheels towards middle so robot turns on the spotTurnSteering.
        Takes angles from 0 - maxTurn (max based on servo max position limits)
    """
    leftAngle = 90 + angle
    rightAngle = 90 - angle

    setSteeringFrontLeft(leftAngle)
    setSteeringFrontRight(rightAngle)
    setSteeringRearLeft(leftAngle)
    setSteeringRearRight(rightAngle)
    

def setSteeringStraight():
    """ Sets all wheels pointing straight ahead
    """
    setSteeringFrontLeft(90)
    setSteeringFrontRight(90)
    setSteeringRearLeft(90)
    setSteeringRearRight(90)
    
    
def main():
    """ Test function for servos and motors
    setSteeringFrontLeft(130) #44
    setSteeringFrontRight(130) #40
    setSteeringRearLeft(130) #41
    setSteeringRearRight(130) #40
    """
    setSteeringStraight()
    
if __name__ == '__main__':
    main()