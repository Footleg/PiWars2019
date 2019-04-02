#!/usr/bin/env python3

import pygame, random, time
import RobotControl as rc
import AutonomousDriving as ad
import dartShooter as ds
from PygameController import RobotController
from enum import Enum
from os import system
import Sensors, ledMatrixDisplays

class Mode(Enum):
    """ Modes Enum class """
    menu = 0
    manual = 1
    sensorsTest = 2
    wallFollowing = 3
    hubbleChallenge = 4
    
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
angle = 90
screen = None
stopProgram = False
debugInfo = 2 #Default to showing robot graphic (reset to 0 if running on HyperPixel display)

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

#Hat editable parameters
hatEditTracker = 0
defaultPowerLevel = 30
autoCycles = 1
steeringLook = True
eyesPos = 0 #Stores which direction eyes are looking (so the LEDs are not repeatedly updated to same pattern)

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
    
    if mode == Mode.manual:
        #Reset steering servos straight if angle is 90 in case we have been in spot steering mode
        if angle == 90:
            setSteering(0)
            
        speedL = -100 * valUD
        speedR = speedL
        rc.setLeftMotorPower(speedL)
        rc.setRightMotorPower(speedR)


def rightStickChangeHandler(valLR, valUD):
    """ Handler function for right analogue stick.
        Controls steering using Left/Right stick position
    """
    global angle
    
    if mode == Mode.manual:
        #Turn off motors if in spot turn mode and manual stick steering is activated
        if rc.motorPowerL == -rc.motorPowerR:
            rc.setLeftMotorPower(0)
            rc.setRightMotorPower(0)
            
        angle = valLR * 40
        setSteering(angle)


def leftTriggerChangeHandler(value):
    """ Handler for left trigger.
        If not turning then controls spot turning.
    """
    global angle
    
    if mode == Mode.manual:
        #if angle == 0:
            rc.spotTurnSteering(40)
            angle = 90 #Indicates spot steering servo position are set
            speedR = (value + 1) * 50
            speedL = -speedR
            rc.setLeftMotorPower(speedL)
            rc.setRightMotorPower(speedR)
            if steeringLook == True:
                eyes.addFrame(ledMatrixDisplays.eye_downright,1)
                eyes.addFrame(ledMatrixDisplays.eye_downleft,2)
    
    
def rightTriggerChangeHandler(value):
    """ Handler for right trigger.
        If not turning then controls spot turning.
    """
    global angle
    
    if mode == Mode.manual:
        #if angle == 0:
            rc.spotTurnSteering(40)
            angle = 90 #Indicates spot steering servo position are set
            speedL = (value + 1) * 50
            speedR = -speedL
            rc.setLeftMotorPower(speedL)
            rc.setRightMotorPower(speedR)
            if steeringLook == True:
                eyes.addFrame(ledMatrixDisplays.eye_downright,1)
                eyes.addFrame(ledMatrixDisplays.eye_downleft,2)
    

def hatChangeHandler(valLR,valUD):
    """ Handler for HAT control on game controller
        Allows parameters to be updated
    """
    global hatEditTracker, defaultPowerLevel, autoCycles
    
    textsize = 30
    settingCount = 9
    
    if valUD != 0:
        hatEditTracker += valUD
        if hatEditTracker < 0:
            hatEditTracker = settingCount
        elif hatEditTracker > settingCount:
            hatEditTracker = 0
    
    pygame.draw.rect(screen, Colour.Purple.value, pygame.Rect(10,440,400,30))
    #showText(screen, "HatEdit: {}".format(hatEditTracker), (300,442), size=textsize)
    
    if hatEditTracker == 1:
        #Update power level
        defaultPowerLevel += (10 * valLR)
        if defaultPowerLevel < 20:
            defaultPowerLevel = 20
        elif defaultPowerLevel > 90:
            defaultPowerLevel = 90
        showText(screen, "Default Power Level: {}".format(defaultPowerLevel), (10,442), size=textsize)
    elif hatEditTracker == 2:
        #Update minimum side sensor distance
        ad.updateMinSideDist(10 * valLR)
        showText(screen, "Min. side sensor dist: {}".format(ad.minSideDist), (10,442), size=textsize)     
    elif hatEditTracker == 3:
        #Update maximum side sensor distance
        ad.updateMaxSideDist(10 * valLR)
        showText(screen, "Max. side sensor dist: {}".format(ad.maxSideDist), (10,442), size=textsize)     
    elif hatEditTracker == 4:
        #Update minimum front sensor distance
        ad.updateMinFrontDist(10 * valLR)
        showText(screen, "Min. front sensor dist: {}".format(ad.minFrontDist), (10,442), size=textsize)     
    elif hatEditTracker == 5:
        #Update auto cycle length
        autoCycles += (5 * valLR)
        if autoCycles < 5:
            autoCycles = 5
        elif autoCycles > 1000:
            autoCycles = 1000
        showText(screen, "No. auto cycles before controller read: {}".format(autoCycles), (10,442), size=textsize)     
    elif hatEditTracker == 6:
        #Update max auto steering angle
        ad.updateMaxSteeringAngle(5 * valLR)
        showText(screen, "Max auto steer angle: {}".format(ad.maxSteeringAngle), (10,442), size=textsize)     
    elif hatEditTracker == 7:
        #Update PID tuning Pk
        ad.updatePk(0.05 * valLR)
        showText(screen, "PID Pk: {}".format(ad.Pk), (10,442), size=textsize)     
    elif hatEditTracker == 8:
        #Update PID tuning Ik
        ad.updateIk(0.01 * valLR)
        showText(screen, "PID Ik: {}".format(ad.Ik), (10,442), size=textsize)     
    elif hatEditTracker == 9:
        #Update PID tuning Dk
        ad.updateDk(0.01 * valLR)
        showText(screen, "PID Dk: {}".format(ad.Dk), (10,442), size=textsize)     


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
        debugInfo += 1
        if debugInfo > 2:
            debugInfo = 0
        
        rc.showRobotGraphic = (debugInfo > 0)
            
    #Reset background if turning debug info off (to clear displayed info)
    if debugInfo == 0:
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
    
    
def triangleBtnHandler(state):
    """ Handler for Triangle button on game controller """
    if state == 1 :
        armShooter()
    
    
def squareBtnHandler(state):
    """ Handler for Square button on game controller """
    if state == 1 :
        disarmShooter()
    
    
def crossXBtnHandler(state):
    """ Handler for Cross button on game controller 
        Trigger dart firing mechanism if active,
        else reset armed flag
    """
    if state == 1 :
        if ds.motorRunning:
            fireDart()
        else:
            ds.armed = False
    
    
def armShooter():
    """ Start up shooter module (in manual mode only)
    """
    if mode == Mode.manual:
        ds.laserOn()
        eyes.showNow(ledMatrixDisplays.red_cross)
        ds.armESC()
        eyes.showNow(ledMatrixDisplays.target)
        ds.motorOn()
        steeringLook = False
        
    
def disarmShooter():
    """ Shut down shooter module """
    global eyesPos
    
    ds.motorOff()
    ds.laserOff()
    eyes.addFrame(ledMatrixDisplays.eye_open)
    eyesPos = 0
    steeringLook = True
    
    
def fireDart():
    """ Trigger shooter """
    ds.fire()

    
def mouseDownHandler(pos, btn):
    """ Handler function for mouse down.
        Determine which menu control was clicked using mouse position for each menu level
    """
    global stopProgram
    global clickSequence

    if mode == Mode.menu:
        if btn == 1:
            #Left-click (or Touchscreen press)
            btn = getMenuBtn(pos)
            
            if menu == MenuLevel.top :
                if btn == 0 :
                    setMode(Mode.manual)
                elif btn == 1 :
                    setMode(Mode.sensorsTest)
                elif btn == 2 :
                    setMode(Mode.wallFollowing)
                elif btn == 3 :
                    setMode(Mode.hubbleChallenge)
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
    global steeringLook
    
    powerLimit = defaultPowerLevel
    secondLevelAddn = int( (100 - defaultPowerLevel) * 1 / 3 )
    thirdLevelAddn = 100 - defaultPowerLevel - secondLevelAddn
    
    if leftBtn1Pressed:
        powerLimit += secondLevelAddn
        
    if rightBtn1Pressed:
        powerLimit += thirdLevelAddn
        
    rc.setMotorPowerLimit(powerLimit)
    
    #Update motor speeds for new power limit level
    rc.setLeftMotorPower(rc.motorPowerL)
    rc.setRightMotorPower(rc.motorPowerR)
    
    #Set eyes to red if power boosted
    if powerLimit > defaultPowerLevel:
        steeringLook = False
        eyes.addFrame(ledMatrixDisplays.red_eye_narrow)
    else:
        steeringLook = True
        eyes.addFrame(ledMatrixDisplays.eye_open)
        eyesPos = 0

    
def showImage(screen,filename, position = [0,0]):
    """ Displays an image on the display at the specified coordinates
        If no coordinates specified then will position at top left
    """
    try:
        image = pygame.image.load( filename ).convert()
        screen.blit( image, position )
        #print("Image placed at {}".format(position) )
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
    
    
def showSensorGraphics(leftDist, rightDist, frontDist):
    setModeBackground()
    scale = 1
    rc.drawVirtualRobot(screen)
    leftSource = (360,190)
    leftEnd1 = (360 - leftDist/scale,190-20)
    leftEnd2 = (360 - leftDist/scale,190+20)
    rightSource = (440,190)
    rightEnd1 = (440 + rightDist/scale,190-20)
    rightEnd2 = (440 + rightDist/scale,190+20)
    frontSource = (400,200)
    frontEnd1 = (400-20,200 - frontDist/scale)
    frontEnd2 = (400+20,200 - frontDist/scale)
    pygame.draw.polygon(screen, Colour.Yellow.value, [leftSource,leftEnd1,leftEnd2])
    pygame.draw.polygon(screen, Colour.Yellow.value, [rightSource,rightEnd1,rightEnd2])
    pygame.draw.polygon(screen, Colour.Yellow.value, [frontSource,frontEnd1,frontEnd2])
    textsize = 20
    showText(screen, "{}".format(leftDist), leftSource, size=textsize)
    showText(screen, "{}".format(rightDist), rightSource, size=textsize)
    showText(screen, "{}".format(frontDist), frontSource, size=textsize)
    

def showDebugData():
    textsize = 38
    lineHeight = 24
    cursor = (10,280)
    pygame.draw.rect(screen, Colour.Purple.value, pygame.Rect(10,280,480,160))
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
        showText(screen, "Wall Avoid", (borderX+2*sepX+34,borderY+185), Colour.Blue, 30, True )
        showImage( screen, "neptune_btn180.gif", (borderX,borderY+sepY) )
        showText(screen, "Hubble", (borderX+55,borderY+sepY+185), Colour.Blue, 30, True )
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
      

def setModeBackground():
    """ Sets the display background for the current mode """
    if mode == Mode.manual :
        showImage( screen, "iss_solar_panel_orange.jpg" )
    elif mode == Mode.sensorsTest :
        showImage( screen, "iss_solar_panel.jpg" )
    elif mode == Mode.wallFollowing :
        showImage( screen, "iss_solar_panel.jpg" )
    elif mode == Mode.hubbleChallenge :
        showImage( screen, "LagoonNebula.jpg" )


def getMenuBtn(pos):
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
    """ Sets up robot for specified mode. """
    global mode
    
    #Stop hardware
    rc.stopAll()
    disarmShooter() #This also restores led matrices to eye_open pattern
    
    #Update global mode
    mode = newMode
    
    #Update display for active mode
    if mode == Mode.menu :
        Sensors.stopAll()
        showMenu(MenuLevel.top)
    else:
        #Initialise screen and hardware for all operating modes
        setModeBackground()
        
        if mode == Mode.manual :
            initDriving()
        elif mode == Mode.sensorsTest :
            Sensors.startAll()
        elif mode == Mode.wallFollowing :
            ad.targetWallDistance = 0 #Reset
            ad.initialisePID()
            Sensors.startAll()
            initDriving()
        elif mode == Mode.hubbleChallenge :
            #Initialise pixy
            Sensors.startAll()
            initDriving()
            

def initDriving():
    """ Initialise robot for driving modes """
    #Reset steering to straight ahead (powers up servos)
    setSteering(0)
    #Initialise power limiting
    updatePowerLimiting()


def setSteering(angle):
    """ Local method to update eyes before passing steering to robot control module """
    global eyesPos
    
    rc.setSteering(angle)
    print(angle)
    
    if steeringLook == True:
        #Set eyes based on steering
        if angle < -10:
            if eyesPos != -1:
                eyes.addFrame(ledMatrixDisplays.eye_downleft)
                eyesPos = -1
        elif angle > 10:
            if eyesPos != 1:
                eyes.addFrame(ledMatrixDisplays.eye_downright)
                eyesPos = 1
        else:
            if eyesPos != 0:
                eyes.addFrame(ledMatrixDisplays.eye_open)
                eyesPos = 0


def main():
    global screen, debugInfo, autoCycles, eyes
    
    virtual = True #Tracks whether running on real robot or digital twin virtual robot simulation
    
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
            leftTriggerChanged = leftTriggerChangeHandler,
            rightTriggerChanged = rightTriggerChangeHandler,
            hatChanged = hatChangeHandler,
            selectBtnChanged = selectBtnHandler,
            startBtnChanged = startBtnHandler,
            homeBtnChanged = homeBtnHandler,
            leftBtn1Changed = leftBtn1Handler, 
            rightBtn1Changed = rightBtn1Handler, 
            triangleBtnChanged = triangleBtnHandler,
            squareBtnChanged = squareBtnHandler,
            crossXBtnChanged = crossXBtnHandler,
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
                #Default to not show debug info when on HyperPixel (on real robot)
                debugInfo = 0
                virtual = False
                autoCycles = 50
                
            robotControl.screen = pygame.display.set_mode(screen_size,display_mode)
            screen = robotControl.screen
            # Create LED matrix display instance after pygame display is defined for virtual LED display to work
            eyes = ledMatrixDisplays.LEDMatrixDisplays()
            # Display eyes on LED matrix displays
            eyes.addFrame(ledMatrixDisplays.eye_open)
            # Initialise whether to display robot graphic
            rc.showRobotGraphic = (debugInfo > 0)
            #Initialise tof sensors
            Sensors.initialise()

            setMode(Mode.menu)
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        frame = 0
        blinkCounter = 0
        blinkPause = 0
        timeC = time.perf_counter() 
        while keepRunning == True :
            frame += 1
            #message = "Speed: {}, Steering: {}".format(speed,angle)
            #robotControl.message = message
            
            #Exit to menu if both select and start buttons are held down at the same time
            if selectBtnPressed and startBtnPressed:
                setMode(Mode.menu)

            #Check for controller button combinations and queue up animations in different modes
            if mode == Mode.menu :
                #Queue up blink after random number of frames
                if blinkCounter == 0:
                    blinkPause = random.randint(100,250)
                blinkCounter += 1
                if blinkCounter > blinkPause:
                    blinkCounter = 0
                    eyes.blink()
            elif mode == Mode.manual :
                if debugInfo == 1:
                    #Display debugging info on screen relevent to mode
                    showDebugData()
            elif mode == Mode.sensorsTest :
                #Get sensor readings and display on screen
                leftDist = Sensors.readDistance(1)
                rightDist = Sensors.readDistance(2)
                frontDist = Sensors.readDistance(3)
                showSensorGraphics(leftDist, rightDist, frontDist)
                
            elif mode == Mode.wallFollowing :
                #Run preset number of cycles of auto driving code before dropping back to main robot loop
                #Controller will not respond in inside this loop. Loop exits if front sensor detects obstackle.
                for a in range( autoCycles ):
                    #Update steering and motors based on sensor readings
                    #print("Loop time: {:.2f}".format( time.perf_counter() - timeC ) )
                    #timeC = time.perf_counter()

                    leftDist = Sensors.readDistance(1)
                    rightDist = Sensors.readDistance(2)
                    frontDist = Sensors.readDistance(3)
                    #print("Sensors read time: {:.2f}".format( time.perf_counter() - timeC ) )
                    
                    #Update robot based on autonomous driving algorithm 
                    ad.wallMidPointPID(leftDist, rightDist, frontDist)
                    if debugInfo > 0:
                        showSensorGraphics(leftDist, rightDist, frontDist)
                    if debugInfo == 1:
                        #Display debugging info on screen relevent to mode
                        showDebugData()
                    #Break from inner auto cycle loop if front sensor distance below min
                    if frontDist < ad.minFrontDist:
                        break
                    
            elif mode == Mode.hubbleChallenge :
                #Run preset number of cycles of auto driving code before dropping back to main robot loop
                #Controller will not respond in inside this loop. Loop exits if front sensor detects obstackle.
                for a in range( autoCycles ):
                    frontDist = Sensors.readDistance(3)
                    if debugInfo > 0:
                        showSensorGraphics(leftDist, rightDist, frontDist)
                    if debugInfo == 1:
                        #Display debugging info on screen relevent to mode
                        showDebugData()
                    #Break from inner auto cycle loop if front sensor distance below min
                    if frontDist < ad.minFrontDist:
                        break
                    
                        
            #Update led RGB matrix displays with next frame of any queued animation
            if frame > 2:
                eyes.showNext()
                frame = 0
            elif virtual:
                #Re-render current image on screen (only needed for virtual displays)
                eyes.reshow()
            pygame.display.flip()
            #print("Trigger Events: {}".format( time.perf_counter() ) )
                
            #Trigger stick events and check for quit
            keepRunning = robotControl.controllerStatus() and not stopProgram
            
            #print("Events Completed: {}".format( time.perf_counter() ) )
    
    finally:
        #Clean up and turn off hardware (motors)
        rc.stopAll()
        #Clear rgb matrix displays
        eyes.clear()
        pygame.quit()


if __name__ == '__main__':
    main()