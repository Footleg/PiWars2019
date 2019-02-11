#!/usr/bin/env python3
""" Mock of AdaFruit PWM board for PiWars 2019 robot Rocky Rover testing

    The robot motors (drive wheels and steering servos) are all controlled from
    an AdaFruit 16-channel 12-bit PWM/Serdo driver board. This hardware mocking
    module displays a virtual model of the robot on the screen and shows the
    wheel speeds and servo positions graphically on the GUI instead of controlling
    the physical robot. The PWM i2c hardware board is not required to run the code
    using this mocking module, so development and testing can be done without the
    actual robot being present.
"""
import time, pygame

#Set servo min and max pulse length for the range of rotation of the servo model being used
servoMin = 105  #105 Min pulse length (out of 4096)
servoMax = 475  #500 Max pulse length (out of 4096)
servoRange = 180 #Rotation range in degrees of the servos being used

#Virtual hardware channels for mock robot
servoChFL = 0
servoChFR = 1
servoChBL = 2
servoChBR = 3

#Globals to store positions of servos and motor speeds
motorSpeedL = 0
motorSpeedR = 0
servoPosFL = 0
servoPosFR = 0
servoPosBL = 0
servoPosBR = 0


def setServoPosition(channel, position):
    """ Sets the position of a servo in degrees
    """
    
    #Convert position in degrees to value in range min-max
    pulse = int( ( (servoMax - servoMin) * position / servoRange ) + servoMin)
    
    if (pulse < servoMin) or (pulse > servoMax):
        print("Calculated servo pulse {} is outside supported range of {} to {}".format(pulse,servoMin,servoMax) )
    else:
        print("Setting servo {} pulse to {}".format(channel,pulse) )
        validChannel = True
        if channel == servoChFL:
            servoPosFL = position
        elif channel == servoChFR:
            servoPosFR = position
        elif channel == servoChBL:
            servoPosBL = position
        elif channel == servoChBR:
            servoPosBR = position
        else:
            validChannel = False
            displayError("Call to set servo position on channel {} which has no servo attached.".format(channel))
            
        if validChannel:
            drawVirtualRobot()
        
    
def setPercentageOn(channel, percent):
    """ Sets the percentage of time a channel is on per cycle.
        For use with PWM motor speed control.
    """
    
    #Fully on pulse length is 4096.
    #With 8V supply and 6V motors, limit to 75% of fully on
    maxPulse = 3072
    
    #Convert percentage to pulse length
    pulse = int( percent * maxPulse / 100 )
    
    #Limit pulse length to between zero and maximum
    if (percent < 0):
        pulse = 0
    elif (percent > 100):
        pulse = maxPulse

    print("Setting servo {} pulse to {}".format(channel,pulse) )
    # pwm.setPWM(channel, 0, pulse)
    
    
def drawVirtualRobot():
    global motorSpeedL, motorSpeedR
    """
    servoPosFL
    servoPosFR
    servoPosBL
    servoPosBR
    """
    screen = pygame.display.get_surface()
    image = pygame.image.load( "moon_btn180.gif" ).convert()
    screen.blit( image, [380, 230] )

    
def displayError(message):
    screen = pygame.display.get_surface()
    screen.fill( (0,0,0) )
    font = pygame.font.Font(None, 32)
    textBitmap = font.render(message, True, [255,0,0] )
    screen.blit( textBitmap, (20, 200) )
    
def main():
    """ Test function for module
    """
    print("""This module cannot run stand alone. Use it from within a pygame application where
the screen has been initialised.""")
  
    
if __name__ == '__main__':
    main()