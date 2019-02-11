#!/usr/bin/env python3

import pygame
import RobotControl as rc
from PygameController import RobotController
from enum import Enum


class Mode(Enum):
    """ Modes Enum class """
    menu = 0
    manual = 1
    automaze = 2
    
class MenuLevel(Enum):
    """ MenuLevel Enum class.
        Values used to control what menu items to display and now to respond to clicks
    """
    top = 0
    close = 1
    
    
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
stopProgram = False

menu = MenuLevel.top
borderX = 50
borderY = 35
sepX = 250
sepY = 225
clickSequence = 0 #Used to track screen clicks to return to menus from running modes

    
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
    global stopProgram
    global clickSequence

    if mode == Mode.menu:
        if btn == 1:
            #Left-click (or Touchscreen press)
            btn = getBtn(pos)
            
            if menu == MenuLevel.top :
                if btn == 0 :
                    setMode(Mode.manual)
                elif btn == 5 :
                    showMenu(MenuLevel.close)
            elif menu == MenuLevel.close :
                if btn == 0 :
                    #TODO: Change to trigger a shutdown
                    stopProgram = True
                elif btn == 1 :
                    stopProgram = True
                elif btn == 2 :
                    showMenu(MenuLevel.top)
                    
            else:
                showMenu(MenuLevel.close)
                showText(screen,"Btn: {}".format(btn), (10,10) )
        elif btn == 3:
            #Right Click (for testing)
            showImage(screen, "mars_hubble_canyon.jpg")
            showImage(screen, "mars1_btn180.gif", pos)
    else:
        #When not in menu mode, monitor clicks to allow menus to be displayed if all 4 quarters of screen are touched
        if clickSequence == 0:
            #Increment if top left quarter clicked
            if pos[0] < 400 and pos[1] < 240 :
                clickSequence += 1
        elif clickSequence == 1:
            #Increment if top right quarter clicked
            if pos[0] > 400 and pos[1] < 240 :
                clickSequence += 1
            else:
                clickSequence = 0
        elif clickSequence == 2:
            #Increment if top right quarter clicked
            if pos[0] < 400 and pos[1] > 240 :
                clickSequence += 1
            else:
                clickSequence = 0
        elif clickSequence == 3:
            #Reset and also change mode if bottom right quarter clicked
            clickSequence = 0
            if pos[0] > 400 and pos[1] > 240 :
                setMode(Mode.menu)

    
def showImage(screen,filename, position = [0,0]):
    """ Displays an image on the display at the specified coordinates
        If no coordinates specified then will position at top left
    """
    try:
        image = pygame.image.load( filename ).convert()
        screen.blit( image, position )
        print("Image placed at {}".format(position) )
    except: 
        screen.fill( (0,0,0) )
        font = pygame.font.Font(None, 40)
        textBitmap = font.render("Failed to load image: " + filename, True, Colour.Red.value )
        screen.blit( textBitmap, (50, 200) )
    
    
def showText(screen, text, position = [0,0], colour = Colour.White, size = 40 ):
    """ Displays text at the specified coordinates
        If no coordinates specified then will position at top left
    """
    font = pygame.font.Font(None, size)
    textBitmap = font.render(text, True, colour.value )
    screen.blit( textBitmap, position )
    
    
def showMenu(level):
    """ Displays the menu graphics on screen """
    global borderX
    global borderY
    global sepX
    global sepY
    global menu
    
    menu = level
    
    if level == MenuLevel.top :
        # Main menu with top level options
        showImage( screen, "LagoonNebula.jpg" )
        borderX = 50
        borderY = 35
        sepX = 250
        sepY = 225
        showImage( screen, "jupiter1_btn180.gif", (borderX,borderY) )
        showText(screen, "Manual Control", (borderX+20,borderY+185), Colour.Blue, 30 )
        showImage( screen, "venus1_btn180.gif", (borderX+2*sepX,borderY+sepY) )
        showText(screen, "Exit", (borderX+2*sepX+70,borderY+sepY+185), Colour.Blue, 30 )
    elif level == MenuLevel.close :
        # Program exit confirmation menu
        showImage( screen, "LagoonNebula.jpg" )
        borderX = 50
        borderY = 150
        sepX = 250
        showImage( screen, "mercury1_btn180.gif", (borderX,borderY) )
        showText(screen, "Shutdown", (borderX+38,borderY+185), Colour.Blue, 30 )
        showImage( screen, "mars2_btn180.gif", (borderX+sepX,borderY) )
        showText(screen, "Desktop", (borderX+sepX+54,borderY+185), Colour.Blue, 30 )
        showImage( screen, "venus2_btn180.gif", (borderX+2*sepX,borderY) )
        showText(screen, "Cancel", (borderX+2*sepX+54,borderY+185), Colour.Blue, 30 )
    else:
        # (temporary code parked here for showing all 6 menu option buttons in position)
        showImage( screen, "LagoonNebula.jpg" )
        borderX = 50
        borderY = 35
        sepX = 250
        sepY = 225
        showImage( screen, "mercury2_btn180.gif", (borderX,borderY) )
        showImage( screen, "mars_btn180.gif", (borderX+sepX,borderY+sepY) )
        showImage( screen, "venus_btn180.gif", (borderX+2*sepX,borderY) )
        showImage( screen, "jupiter2_btn180.gif", (borderX,borderY+sepY) )
        showImage( screen, "moon_btn180.gif", (borderX+sepX,borderY) )
        showImage( screen, "saturn_btn180.gif", (borderX+2*sepX,borderY+sepY) )
    

def getBtn(pos):
    """ Returns the index of the button which the position matches on the screen menu.
        Returns -1 if no button at position.
    """
    x = pos[0] - borderX
    y = pos[1] - borderY
    btnWidth = 180
    col = -1
    row = -1
    btn = -1
    numCols = 3
    numRows = 2
    
    #Determine button column from X position
    while x > 0 :
        if x < btnWidth :
            #Position inside btn area
            col += 1
            break
        elif x > sepX:
            #Position beyond seperation to next btn area
            x -= sepX
            col += 1
        else:
            #Position in between btn areas
            col = -1
            break
    
    if col >= 0 and col < numCols :
        #Determine button row from Y position
        while y > 0 :
            if y < btnWidth :
                #Position inside btn area
                row += 1
                break
            elif y > sepY:
                #Position beyond seperation to next btn area
                y -= sepY
                row += 1
            else:
                #Position in between btn areas
                row = -1
                break
            
        if row >= 0 and row < numRows :
            btn = (numCols * row) + col
        
    return btn

def setMode(newMode):
    global mode
    
    #Stop hardware
    rc.stopAll()
    
    #Update global mode
    mode = newMode
    
    #Update display for active mode
    if mode == Mode.menu :
        showMenu(MenuLevel.top)
    elif mode == Mode.manual :
        showImage( screen, "iss_solar_panel_orange.jpg" )
        rc.setSteeringFrontLeft(90)
        rc.setSteeringFrontRight(90)
        rc.setSteeringRearLeft(90)
        rc.setSteeringRearRight(90)


def main():
    global screen
    global stopProgram
    
    ## Check that required hardware is connected ##
    
    # Determine screen resolution before pygame window is created
    pygame.init()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h

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
            #Success, we have a game controller connected. Set up screen
            screen_size = [800,480]
            display_mode = 0 #Default to windowed mode
            if (screen_w == screen_size[0]) and (screen_h == screen_size[1]):
                #Run fullscreen for HyperPixel display
                display_mode = pygame.FULLSCREEN
            robotControl.screen = pygame.display.set_mode(screen_size,display_mode)
            screen = robotControl.screen
            robotControl.displayControllerOutput = False
            setMode(Mode.menu)
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            message = "Speed: {}, Steering: {}".format(speed,angle)
            robotControl.message = message
            
            # Trigger stick events and check for quit
            keepRunning = robotControl.controllerStatus() and not stopProgram
    
    finally:
        #Clean up and turn off hardware (motors)
        rc.stopAll()
        pygame.quit()


if __name__ == '__main__':
    main()
