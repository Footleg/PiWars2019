#!/usr/bin/env python3

import AdafruitPWMboard as pwmb
import time

#Define the channels which the servos are connected to
laserChannel = 13
triggerChannel = 14
escChannel = 15

maxMotorPower = int( 180 * 0.6 ) #Above 60% max power the  rubber band comes off motor

triggerOpenPos = 85

triggerClosedPos = 160


def motorOn():
    """ Turns on the dart shooter motor by ramping up power """
    for angle in range(0, maxMotorPower):
        pwmb.setServoPosition(escChannel, angle) 
        time.sleep(0.1)


def motorOff():
    """ Turns off the dart shooter motor """
    pwmb.setPercentageOn(escChannel, 0) #Off
    
    
def laserOn():
    """ Turns off the laser """
    pwmb.setConstantOn(laserChannel)
    

def laserOff():
    """ Turns off the laser """
    pwmb.setPercentageOn(laserChannel, 0) #Off


def fire():
    """ Pushes dart onto flywheel """
    for angle in range(triggerOpenPos, triggerClosedPos, 5):
        pwmb.setServoPosition(triggerChannel, angle) 
        time.sleep(0.05)
    time.sleep(0.5)
    pwmb.setServoPosition(triggerChannel, triggerOpenPos)
    
    
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
        
        fire()
        time.sleep(5)
        fire()
        time.sleep(5)
        fire()
        time.sleep(5)
        laserOn()
        time.sleep(1)

    finally:
        print("Turning off")
        motorOff()
        laserOff()


if __name__ == '__main__':
    main()
