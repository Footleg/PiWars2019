#!/usr/bin/env python3

import sys
sys.path.append('/home/pi/Documents/Python Projects/pygame-controller')

import pygame, random, time, math
import RobotControl as rc
from PygameController import RobotController

#Declare globals
speed = 0
angle = 90

def initStatus(status):
    """ Callback function which displays status during initialisation """
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format( status ) )
            

def leftStickChangeHandler(valLR, valUD):
    """ Handler function for left analogue stick.
        Controls motor speed using Up/Down stick position
    """
    global speed
    
    speed = -100 * valUD
    rc.setLeftMotorPower(speed)
    rc.setRightMotorPower(speed)


def rightStickChangeHandler(valLR, valUD):
    """ Handler function for right analogue stick.
        Controls steering using Left/Right stick position
    """
    global angle
    angle = (-valLR * 40) + 90
    angleRear = (valLR * 40) + 90
    
    rc.setSteeringFrontLeft(angle)
    rc.setSteeringFrontRight(angle)
    rc.setSteeringRearLeft(angleRear)
    rc.setSteeringRearRight(angleRear)
    
def main():
    ## Check that required hardware is connected ##

    # Define which inputs and outputs are configured
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Rocky Rover Remote Control", initStatus,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler)
        
        if cnt.initialised :
            keepRunning = True
            #Indicate success here, we are ready to run
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            message = "Speed: {}, Steering: {}".format(speed,angle)
            cnt.message = message
            
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
    
    finally:
        #Clean up and turn off Blinkt LEDs
        rc.stopAll()
        pygame.quit()


if __name__ == '__main__':
    main()
