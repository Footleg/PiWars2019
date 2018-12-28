#!/usr/bin/env python3

import pygame, random, time, math
import RobotControl as rc
from PygameController import RobotController
from enum import Enum


class Mode(Enum):
    """ Modes Enum class """
    menu = 0
    manual = 1
    automaze = 2
    
    
class Colour(Enum):
    """ Colour definitions Enum class """
    Red = (255,0,0)
    Green = (0,255,0)
    Blue = (0,0,255)
    White = (255,255,255)
    
    
#Declare globals
mode = Mode.menu
speed = 0
angle = 90
screen = None

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
    
    if mode == Mode.manual:
        speed = -100 * valUD
        rc.setLeftMotorPower(speed)
        rc.setRightMotorPower(speed)


def rightStickChangeHandler(valLR, valUD):
    """ Handler function for right analogue stick.
        Controls steering using Left/Right stick position
    """
    global angle
    if mode == Mode.manual:
        angle = (-valLR * 40) + 90
        angleRear = (valLR * 40) + 90
        
        rc.setSteeringFrontLeft(angle)
        rc.setSteeringFrontRight(angle)
        rc.setSteeringRearLeft(angleRear)
        rc.setSteeringRearRight(angleRear)


def mouseDownHandler(pos, btn):
    """ Handler function for mouse down.
        Determine which menu control was clicked using mouse position
    """
    #print("position {}; button {}".format(pos,btn) )
    if mode == Mode.menu:
        if btn == 1:
            showImage(screen, "mars_btn_180.jpg", pos)
            showText(screen, "Manual Control", (200,200) )
        elif btn == 3:
            showImage(screen, "mars_hubble_canyon.jpg")
    
    
def showImage(screen,filename, position = [0,0]):
    """ Displays an image on the display at the specified coordinates
        If no coordinates specified then will position at top left
    """
    try:
        image = pygame.image.load( filename ).convert()
        screen.blit( image, position )
    except: 
        screen.fill( (0,0,0) )
        font = pygame.font.Font(None, 40)
        textBitmap = font.render("Failed to load image: " + filename, True, Colour.Red )
        screen.blit( textBitmap, (50, 200) )
    
    
def showText(screen, text, position = [0,0], colour = Colour.White, size = 40 ):
    """ Displays text at the specified coordinates
        If no coordinates specified then will position at top left
    """
    font = pygame.font.Font(None, size)
    textBitmap = font.render(text, True, colour.value )
    screen.blit( textBitmap, position )
    
    
def main():
    global screen
    
    ## Check that required hardware is connected ##

    # Define which inputs and outputs are configured
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        robotControl = RobotController("Rocky Rover Remote Control", initStatus,
            leftStickChanged = leftStickChangeHandler,
            rightStickChanged = rightStickChangeHandler,
            mouseDown = mouseDownHandler)
        
        if robotControl.initialised :
            keepRunning = True
            #Success, we have a game controller connected. Set up screen for HyperPixel display
            robotControl.screen = pygame.display.set_mode([800,480])
            screen = robotControl.screen
            robotControl.displayControllerOutput = False
            showImage(robotControl.screen,"iss_solar_panel.jpg")
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            message = "Speed: {}, Steering: {}".format(speed,angle)
            robotControl.message = message
            
            # Trigger stick events and check for quit
            keepRunning = robotControl.controllerStatus()
    
    finally:
        #Clean up and turn off hardware (motors)
        rc.stopAll()
        pygame.quit()


if __name__ == '__main__':
    main()
