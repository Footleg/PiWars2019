#!/usr/bin/env python3

import AdafruitPWMboard as pwmb
import time

#Define the channels which the servos are connected to
laserChannel = 13
triggerChannel = 14
escChannel = 15

maxMotorPower = int( 180 * 0.6 ) #Above 60% max power the  rubber band comes off motor


def motorOn():
    """ Turns on the nerf shooter motor by ramping up power """
    for pulse in range(0, maxMotorPower):
        pwmb.setServoPosition(escChannel, pulse) 
        time.sleep(0.1)


def motorOff():
    """ Turns off the nerf shooter motor """
    pwmb.setPercentageOn(escChannel, 0) #Off
    
    
def laserOn():
    """ Turns off the nerf shooter motor """
    pwmb.setConstantOn(laserChannel)
    

def laserOff():
    """ Turns off the nerf shooter motor """
    pwmb.setPercentageOn(laserChannel, 0) #Off
    
    
def main():
    # ===========================================================================
    # Arm ESC and start up motor
    # ===========================================================================
    try:
        print("Setting min pulse to arm (for 2 seconds)")
        pwmb.setServoPosition(escChannel, 0)
        time.sleep(2)
        
        print("Laser on")
        laserOn()
        
        print("Ramping up")
        motorOn()
        
        time.sleep(1)

    finally:
        print("Turning off")
        motorOff()
        laserOff()


if __name__ == '__main__':
    main()
