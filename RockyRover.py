#!/usr/bin/env python3

import pygame
import RobotControl as rc
from PygameController import RobotController
from enum import Enum
from os import system
import Sensors, ledMatrixDisplays

class Mode(Enum):
    """ Modes Enum class """
    menu = 0
    manual = 1
    sensorsTest = 2
    
class MenuLevel(Enum):
    """ MenuLevel Enum class.
        Values used to control what menu items to display and now to respond to clicks
    """
    top = 0
    close = 1
    shutdownReboot = 2
   
class Colour(Enum):
    """ Colour definitions Enum class """
    Red = (255,0,0)
    Green = (0,255,0)
    Blue = (0,0,255)
    Yellow = (255,255,0)
    White = (255,255,255)
    Black = (0,0,0)
    Brown = (120,60,0)
    DarkBlue  = (0,0,200)
    Purple = (100,0,100)
    
    
#Declare globals
mode = Mode.menu
speed = 0
angle = 90
screen = None
stopProgram = False
debugInfo = False

menu = MenuLevel.top
borderX = 50
borderY = 35
sepX = 250
sepY = 225
clickSequence = 0 #Used to track screen clicks to return to menus from running modes
#Trackers of button states on controller
selectBtnPressed = False
startBtnPressed = False
leftBtn1Pressed = False
rightBtn1Pressed = False

    
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


def selectBtnHandler(state):
    """ Handler for Select button on game controller """
    global selectBtnPressed
    selectBtnPressed = state
    
    
def startBtnHandler(state):
    """ Handler for Start button on game controller """
    global startBtnPressed
    startBtnPressed = state
    
    
def homeBtnHandler(state):
    """ Handler for Home button on game controller """
    global debugInfo
    
    #Toggle state of debug info
    if state == True:
        debugInfo = not debugInfo
    
    #Reset background if turning debug info off (to clear displayed info)
    if debugInfo == False:
        setModeBackground()
        
    
def leftBtn1Handler(state):
    """ Handler for Start button on game controller """
    global leftBtn1Pressed
    leftBtn1Pressed = state
    updatePowerLimiting()
    
    
def rightBtn1Handler(state):
    """ Handler for Start button on game controller """
    global rightBtn1Pressed
    rightBtn1Pressed = state
    updatePowerLimiting()
    
    
def mouseDownHandler(pos, btn):
    """ Handler function for mouse down.
        Determine which menu control was clicked using mouse position for each menu level
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
                elif btn == 1 :
                    setMode(Mode.sensorsTest)
                elif btn == 5 :
                    showMenu(MenuLevel.close)
                    
            elif menu == MenuLevel.close :
                if btn == 0 :
                    showMenu(MenuLevel.shutdownReboot)
                elif btn == 1 :
                    #Set flag to exit main program loop
                    stopProgram = True
                elif btn == 2 :
                    showMenu(MenuLevel.top)
                    
            elif menu == MenuLevel.shutdownReboot :
                if btn == 0 :
                    #Cancel where shutdown was, so don't accidently shutdown on a double tap
                    showMenu(MenuLevel.close)
                elif btn == 1 :
                    #Trigger a reboot
                    system("reboot")
                elif btn == 2 :
                    #Trigger a shutdown
                    system("shutdown now")
                    
            else:
                #Should not happen, but in case it does change to a valid menu and show which button was clicked
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

    
def updatePowerLimiting():
    """ Sets the maximum motor power based on controller btn states.
        Default power limit is 40% equivalent of motor driver Vin voltage.
        Holding left button 1 raises limit to 80%
        Holding right button 1 raises limit to 60%
        Holding both left & right button 1 raises limit to 100%
    """
    powerLimit = 30
    
    if leftBtn1Pressed:
        powerLimit += 30
        
    if rightBtn1Pressed:
        powerLimit += 40
        
    rc.setMotorPowerLimit(powerLimit)
    
    #Update motor speeds
    rc.setLeftMotorPower(speed)
    rc.setRightMotorPower(speed)

    
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
    
    
def showText(screen, text, position = [0,0], colour = Colour.White, size = 40, shadow=False, shadowCol=Colour.Black ):
    """ Displays text at the specified coordinates
        If no coordinates specified then will position at top left
    """
    font = pygame.font.Font(None, size)
    
    if shadow:
        textBitmap = font.render(text, True, shadowCol.value )
        screen.blit( textBitmap, (position[0]+1,position[1]+1) )
    
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
        showText(screen, "Manual Control", (borderX+20,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "mars1_btn180.gif", (borderX+sepX,borderY) )
        showText(screen, "Sensor Test", (borderX+sepX+34,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "pluto_btn180.gif", (borderX+2*sepX,borderY) )
        showImage( screen, "neptune_btn180.gif", (borderX,borderY+sepY) )
        showImage( screen, "moon_btn180.gif", (borderX+sepX,borderY+sepY) )
        showImage( screen, "venus1_btn180.gif", (borderX+2*sepX,borderY+sepY) )
        showText(screen, "Exit", (borderX+2*sepX+70,borderY+sepY+185), Colour.Blue, 30, True )
    elif level == MenuLevel.close :
        # Program exit confirmation menu
        showImage( screen, "LagoonNebula.jpg" )
        borderX = 50
        borderY = 150
        sepX = 250
        showImage( screen, "mercury1_btn180.gif", (borderX,borderY) )
        showText(screen, "Shutdown", (borderX+44,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "neptune_btn180.gif", (borderX+sepX,borderY) )
        showText(screen, "Desktop", (borderX+sepX+58,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "saturn_btn180.gif", (borderX+2*sepX,borderY) )
        showText(screen, "Cancel", (borderX+2*sepX+54,borderY+185), Colour.Blue, 30, True )
    elif level == MenuLevel.shutdownReboot :
        # Shutdown/Reboot confirmation menu
        showImage( screen, "LagoonNebula.jpg" )
        borderX = 50
        borderY = 150
        sepX = 250
        showImage( screen, "saturn_btn180.gif", (borderX,borderY) )
        showText(screen, "Cancel", (borderX+58,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "uranus_btn180.gif", (borderX+sepX,borderY) )
        showText(screen, "Reboot", (borderX+sepX+58,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "venus1_btn180.gif", (borderX+2*sepX,borderY) )
        showText(screen, "Shutdown", (borderX+2*sepX+42,borderY+185), Colour.Blue, 30, True )
    

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
    else:
        #Initialise screen and hardware for all operating modes
        setModeBackground()
        #Reset steering to straight ahead (powers up servos)
        rc.setSteeringFrontLeft(90)
        rc.setSteeringFrontRight(90)
        rc.setSteeringRearLeft(90)
        rc.setSteeringRearRight(90)
        #Initialise power limiting
        updatePowerLimiting()
        

def setModeBackground():
    """ Sets the display background for the current mode """
    if mode == Mode.manual :
        showImage( screen, "iss_solar_panel_orange.jpg" )
    elif mode == Mode.sensorsTest :
        showImage( screen, "iss_solar_panel.jpg" )
    

def main():
    global screen
    
    ## Check that required hardware is connected ##
    
    # Determine screen resolution before pygame window is created
    pygame.init()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        robotControl = RobotController("Rocky Rover Remote Control", initStatus,
            leftStickChanged = leftStickChangeHandler,
            rightStickChanged = rightStickChangeHandler,
            selectBtnChanged = selectBtnHandler,
            startBtnChanged = startBtnHandler,
            homeBtnChanged = homeBtnHandler,
            leftBtn1Changed = leftBtn1Handler, 
            rightBtn1Changed = rightBtn1Handler, 
            mouseDown = mouseDownHandler)
        
        if robotControl.initialised :
            keepRunning = True
            robotControl.displayControllerOutput = False
            #Success, we have a game controller connected. Set up screen
            screen_size = [800,480]
            display_mode = 0 #Default to windowed mode
            if (screen_w == screen_size[0]) and (screen_h == screen_size[1]):
                #Run fullscreen for HyperPixel display
                display_mode = pygame.FULLSCREEN
            robotControl.screen = pygame.display.set_mode(screen_size,display_mode)
            screen = robotControl.screen
            # Create LED matrix display instance after pygame display is defined for virtual LED display to work
            eyes = ledMatrixDisplays.LEDMatrixDisplays()
            # Put test frames onto queue
            eyes.addFrame(ledMatrixDisplays.eye_open)
            eyes.addFrame(ledMatrixDisplays.eye_lid1)
            eyes.addFrame(ledMatrixDisplays.eye_lid2)
            eyes.addFrame(ledMatrixDisplays.eye_lid3)
            eyes.addFrame(ledMatrixDisplays.eye_lid2)
            eyes.addFrame(ledMatrixDisplays.eye_lid1)
            eyes.addFrame(ledMatrixDisplays.eye_open)
            eyes.addFrame(ledMatrixDisplays.one)
            setMode(Mode.menu)
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        frame = 0
        while keepRunning == True :
            frame += 1
            message = "Speed: {}, Steering: {}".format(speed,angle)
            robotControl.message = message
            
            #Check for controller button combinations in different modes
            if mode == Mode.manual :
                #Exit to menu if both select and start buttons are held down at the same time
                if selectBtnPressed and startBtnPressed:
                    setMode(Mode.menu)
                elif debugInfo:
                    #Display debugging info on screen relevent to mode
                    textsize = 38
                    lineHeight = 24
                    pygame.draw.rect(screen, Colour.Purple.value, pygame.Rect(10,10,480,160))
                    cursor = (10,10)
                    showText(screen, "Debug Information:", cursor, size=textsize)
                    cursor = (cursor[0]+20,cursor[1]+lineHeight)
                    showText(screen, "Power Limiting: {}%".format( rc.getMotorPowerLimit() ), cursor, size=textsize)
                    cursor = (cursor[0],cursor[1]+lineHeight)
                    showText(screen, "Left motor ch1 pulse len: {}/4096".format( rc.getPWMPulseLength(rc.motorsLeftChannelA) ), cursor, size=textsize)
                    cursor = (cursor[0],cursor[1]+lineHeight)
                    showText(screen, "Left motor ch2 pulse len: {}/4096".format( rc.getPWMPulseLength(rc.motorsLeftChannelB) ), cursor, size=textsize)
                    cursor = (cursor[0],cursor[1]+lineHeight)
                    showText(screen, "Right motor ch1 pulse len: {}/4096".format( rc.getPWMPulseLength(rc.motorsRightChannelA) ), cursor, size=textsize)
                    cursor = (cursor[0],cursor[1]+lineHeight)
                    showText(screen, "Right motor ch2 pulse len: {}/4096".format( rc.getPWMPulseLength(rc.motorsRightChannelB) ), cursor, size=textsize)
                    pygame.display.flip()
            elif mode == Mode.sensorsTest :
                #Get sensor readings and display on screen
                leftDist = Sensors.readDistance(1)
                rightDist = Sensors.readDistance(2)
                frontDist = Sensors.readDistance(3)
                leftSource = (360,190)
                leftEnd1 = (360 - leftDist/4,190-20)
                leftEnd2 = (360 - leftDist/4,190+20)
                rightSource = (440,190)
                rightEnd1 = (440 + rightDist/4,190-20)
                rightEnd2 = (440 + rightDist/4,190+20)
                frontSource = (400,200)
                frontEnd1 = (400-20,200 - frontDist/4)
                frontEnd2 = (400+20,200 - frontDist/4)
                setModeBackground()
                rc.drawVirtualRobot(screen)
                pygame.draw.polygon(screen, Colour.Purple.value, [leftSource,leftEnd1,leftEnd2])
                pygame.draw.polygon(screen, Colour.Purple.value, [rightSource,rightEnd1,rightEnd2])
                pygame.draw.polygon(screen, Colour.Purple.value, [frontSource,frontEnd1,frontEnd2])
                if frame > 1:
                    eyes.showNext()
                    frame = 0
                else:
                    #Re-render current (only needed for onscreen display, but no harm done calling for real displays)
                    eyes.reshow()
                pygame.display.flip()
                
            # Trigger stick events and check for quit
            keepRunning = robotControl.controllerStatus() and not stopProgram
    
    finally:
        #Clean up and turn off hardware (motors)
        rc.stopAll()
        pygame.quit()


if __name__ == '__main__':
    main()
