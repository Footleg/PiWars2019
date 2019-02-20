#!/usr/bin/env python3

""" PiWars Rocky Rover robot control functions module
"""

import AdafruitPWMboard as pwmb
import time

# PWM board channel configuration 
servoFrontLeftChannel = 0
servoFrontRightChannel = 1
servoRearLeftChannel = 2
servoRearRightChannel = 3
motorsLeftChannelA = 12
motorsLeftChannelB = 13
motorsRightChannelA = 15
motorsRightChannelB = 14

# Servo calibration constants
servoFrontLeftOffset = 32 #14 <- plywood prototype
servoFrontRightOffset = -11 #36 <- plywood prototype
servoRearLeftOffset = 14 #16 <- plywood prototype
servoRearRightOffset = 24 #24 <- plywood prototype

servoMinAngle = 40
servoMaxAngle = 135


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
    
    
#==========================================================================================
# Motor Control Functions, using a pair of channels
#==========================================================================================
def setMotorPowerLimit(percentage):
    pwmb.setMotorPowerLimiting(percentage)
    

def getMotorPowerLimit():
    return pwmb.motorPowerLimiting
    

def getPWMPulseLength(channel):
    return pwmb.channelPulseLengths[channel]
    

def setMotorPower(channelA, channelB, power):
    """ Uses a pair of pwm channels to send switching logic pulses to motor driver.
        One channel is set to low (zero pulse width) and the other to a percentage on.
    """
    if power > 0:
        pwmb.setPercentageOn(channelA, 0)
        pwmb.setPercentageOn(channelB, power)
    elif power < 0:
        pwmb.setPercentageOn(channelB, 0)
        pwmb.setPercentageOn(channelA, -power)
    else:
        pwmb.setPercentageOn(channelA, 0)
        pwmb.setPercentageOn(channelB, 0)

def setLeftMotorPower(power):
    setMotorPower(motorsLeftChannelA, motorsLeftChannelB, power)
    
def setRightMotorPower(power):
    setMotorPower(motorsRightChannelA, motorsRightChannelB, power)
    
def stopAll():
    pwmb.allOff()
    
    
def main():
    """ Test function for servos and motors
    setSteeringFrontLeft(130) #44
    time.sleep(1)
    setSteeringFrontRight(130) #40
    time.sleep(1)
    setSteeringRearLeft(130) #41
    time.sleep(1)
    setSteeringRearRight(130) #40
    time.sleep(1)
    setSteeringStraight()
    time.sleep(1)
    setLeftMotorPower(30)
    time.sleep(1)
    setLeftMotorPower(-30)
    time.sleep(1)
    setLeftMotorPower(0)
    setRightMotorPower(30)
    time.sleep(1)
    setRightMotorPower(-30)
    time.sleep(1)
    setRightMotorPower(0)
    """
    setSteeringStraight()
    speed = 50
    setLeftMotorPower(speed)
    setRightMotorPower(speed)
    time.sleep(1)
    stopAll()    
    time.sleep(0.25)
    speed = -50
    setLeftMotorPower(speed)
    setRightMotorPower(speed)
    time.sleep(1)
    
    stopAll()    
    
if __name__ == '__main__':
    main()