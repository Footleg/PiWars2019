#!/usr/bin/env python3

""" PiWars Rocky Rover robot control functions module
"""

from sentinelboard import SentinelBoard
import pygame, statistics, time


sb = SentinelBoard()

# Set voltage reading calibration for this specific board
sb.sbHardware.voltage_multiplier = 1.125

# PWM board channel configuration 
servoFrontLeftChannel = 0
servoFrontRightChannel = 1
servoRearLeftChannel = 2
servoRearRightChannel = 3

# Servo calibration constants
servoFrontLeftOffset = 32 #14 <- plywood prototype
servoFrontRightOffset = -11 #36 <- plywood prototype
servoRearLeftOffset = 14 #16 <- plywood prototype
servoRearRightOffset = 24 #24 <- plywood prototype

servoMinAngle = 40
servoMaxAngle = 135

#Globals to store positions servos have been set to
servoPosFL = 80
servoPosFR = 100
servoPosBL = 110
servoPosBR = 70

#Globals to store power levels motors have been set to
motorPowerL = 0
motorPowerR = 0

showRobotGraphic = False

voltage_readings = []
firstSetVoltReadings = True
timeSinceLastRead = 0

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
    sb.setServoPosition(servoChannel, servoPos)
    
    if showRobotGraphic:
        drawVirtualRobot( pygame.display.get_surface() )
    
    
def setSteeringFrontLeft(angle):
    """ Sets the position of the front left steering servo """
    global servoPosFL
    
    setSteeringLegPositionSafely(angle, servoFrontLeftChannel, servoFrontLeftOffset)
    servoPosFL = angle
    
    
def setSteeringFrontRight(angle):
    """ Sets the position of the front right steering servo """
    global servoPosFR
    
    setSteeringLegPositionSafely(angle, servoFrontRightChannel, servoFrontRightOffset)
    servoPosFR = angle
    
    
def setSteeringRearLeft(angle):
    """ Sets the position of the rear left steering servo """
    global servoPosBL
    
    setSteeringLegPositionSafely(angle, servoRearLeftChannel, servoRearLeftOffset)
    servoPosBL = angle
    
    
def setSteeringRearRight(angle):
    """ Sets the position of the rear right steering servo """
    global servoPosBR
    
    servoPosBR = angle
    setSteeringLegPositionSafely(angle, servoRearRightChannel, servoRearRightOffset)
    #print("Rear Right angle: {}".format(angle) )
    
    
def setSteering(angle):
    """ Sets wheels to an angle to drive in a curve """
    frontAngle = -angle + 90
    rearAngle = angle + 90
    setSteeringFrontLeft(frontAngle)
    setSteeringFrontRight(frontAngle)
    setSteeringRearLeft(rearAngle)
    setSteeringRearRight(rearAngle)


def spotTurnSteering(angle):
    """ Turns all wheels towards middle so robot turns on the spotTurnSteering.
        Takes angles from 0 - maxTurn (max based on servo max position limits)
    """
    leftAngle = 90 + angle
    rightAngle = 90 - angle

    setSteeringFrontLeft(rightAngle)
    setSteeringFrontRight(leftAngle)
    setSteeringRearLeft(leftAngle)
    setSteeringRearRight(rightAngle)
    
    
def turn90Deg(clockwise=True):
    """ Turn 90 degrees on the spot) """
    spotTurnSteering(40)
    if clockwise == False:
        speedR = 100
    else:
        speedR = -100
    speedL = -speedR
    setLeftMotorPower(speedL)
    setRightMotorPower(speedR)
    sb.watchdogPause(0.6)
    setSteering(0)
    setLeftMotorPower(0)
    setRightMotorPower(0)
    
    
#==========================================================================================
# Motor Control Functions, using a pair of channels
#==========================================================================================
def setMotorPowerLimit(percentage):
    #Cap maximum percentage to 100 or PWM board does not output
    if percentage > 100:
        percentage = 100
    sb.setMotorPowerLimiting(percentage)
    

def getMotorPowerLimit():
    return sb.motorPowerLimiting
    

def getMotorSupplyVoltage(readingsAv = 10):
    global timeSinceLastRead, firstSetVoltReadings

    # Only read if over 10 s since last reading
    timenow = time.time()
    if timenow - timeSinceLastRead > 1:
        timeSinceLastRead = timenow

        readings = []
        for i in range(readingsAv):
            motorV = sb.sbHardware.motor_voltage
            readings.append(motorV)

        avReading = statistics.median(readings)

        if len(voltage_readings) > 9:
            #Throw out any bad readings from array
            if firstSetVoltReadings:
                avSet = statistics.mean(voltage_readings)
                print(f"Set average: {avSet}")
                for idx in range(len(voltage_readings)-1,0,-1):
                    print(f"Scanning {idx} value: {voltage_readings[idx]}")
                    if abs(voltage_readings[idx]-avSet)/avSet > 0.2:
                        #Remove reading which is 20% off median
                        voltage_readings.pop(idx)
                        print(f"Removed {idx}")
                if len(voltage_readings) > 9:
                    #Step cleaning set when all values are reasonable
                    firstSetVoltReadings = False
                
            #Take average and only accept new reading if within 5% of it
            prevAvReading = statistics.mean(voltage_readings)

            if abs(avReading-prevAvReading)/prevAvReading < 0.05:
                #Remove first item and add new one
                voltage_readings.pop(0)
                voltage_readings.append(avReading)
        else:
            # Just add reading to array
            voltage_readings.append(avReading)

    return statistics.mean(voltage_readings)


def getPWMPulseLength(channel):
    return sb.sbHardware.channelPulseLengths[channel]


def setLeftMotorPower(power):
    global motorPowerL
    
    sb.setMotorPower(1, power)
    motorPowerL = power
    
    if showRobotGraphic:
        drawVirtualRobot( pygame.display.get_surface() )
    
    
def setRightMotorPower(power):
    global motorPowerR
    
    sb.setMotorPower(2, power)
    motorPowerR = power
    
    if showRobotGraphic:
        drawVirtualRobot( pygame.display.get_surface() )
    
    
def stopAll():
    sb.sbHardware.allOff()
    
    
def drawVirtualRobot(screen):
    """ Draw graphical representation of robot on screen, indicating wheel positions and motor speeds """
    
    if screen != None:
        #Reset screen with a background image
        image = pygame.image.load( "mars_hubble_canyon.jpg" ).convert()
        screen.blit( image, [0, 0] )
        
        #Draw body of robot
        BLACK = [0,0,0]
        BROWN = [120,60,0]
        RED   = [255,0,0]
        BLUE  = [0,0,200]
        PURPLE = [100,0,100]
        WHEEL_W = 30
        WHEEL_H = 70
        pygame.draw.rect(screen, BLUE, pygame.Rect(335,145,130,175))
        pygame.draw.rect(screen, BLUE, pygame.Rect(365,30,70,115))
        pygame.draw.rect(screen, BLUE, pygame.Rect(290,160,220,16))
        pygame.draw.rect(screen, BLUE, pygame.Rect(296,100,20,280))
        pygame.draw.rect(screen, BLUE, pygame.Rect(484,100,20,280))
        pygame.draw.rect(screen, BLUE, pygame.Rect(270,220,30,18))
        pygame.draw.rect(screen, BLUE, pygame.Rect(500,220,30,18))
        pygame.draw.rect(screen, BLACK, pygame.Rect(240,195,WHEEL_W,WHEEL_H))
        pygame.draw.rect(screen, BLACK, pygame.Rect(530,195,WHEEL_W,WHEEL_H))
            
        #Draw rotated wheels
        CIRCLE_DIA = 8
        WHEEL_L_X = 306
        WHEEL_R_X = 494
        WHEEL_F_Y = 62
        WHEEL_B_Y = 418
        #Adjust for 90 degrees being zero position of virtual wheels, and apply servo calibration offsets
        drawRotatedRectangle(screen,WHEEL_L_X,WHEEL_B_Y,WHEEL_W,WHEEL_H,90-servoPosBL,BLACK)
        pygame.draw.circle(screen, RED,(WHEEL_L_X,WHEEL_B_Y),CIRCLE_DIA)
        drawRotatedRectangle(screen,WHEEL_R_X,WHEEL_B_Y,WHEEL_W,WHEEL_H,90-servoPosBR,BLACK)
        pygame.draw.circle(screen, RED,(WHEEL_R_X,WHEEL_B_Y),CIRCLE_DIA)
        drawRotatedRectangle(screen,WHEEL_L_X,WHEEL_F_Y,WHEEL_W,WHEEL_H,90-servoPosFL,BLACK)
        pygame.draw.circle(screen, RED,(WHEEL_L_X,WHEEL_F_Y),CIRCLE_DIA)
        drawRotatedRectangle(screen,WHEEL_R_X,WHEEL_F_Y,WHEEL_W,WHEEL_H,90-servoPosFR,BLACK)
        pygame.draw.circle(screen, RED,(WHEEL_R_X,WHEEL_F_Y),CIRCLE_DIA)
        
        #Display motor speeds
        font = pygame.font.Font(None, 28)
        motorSpeedL = motorPowerL
        textBitmap = font.render("{}%".format(motorSpeedL), True, RED )
        arrowLength = 20 + abs(motorSpeedL * 2)
        arrowTop = 230-(arrowLength/2)
        pygame.draw.rect(screen, PURPLE, pygame.Rect(160,arrowTop,30,arrowLength))
        if motorSpeedL > 0:
            pygame.draw.polygon(screen, PURPLE, [(175,arrowTop-30),(145,arrowTop),(205,arrowTop)])
        elif motorSpeedL < 0:
            arrowBot = arrowTop + arrowLength
            pygame.draw.polygon(screen, PURPLE, [(175,arrowBot+30),(145,arrowBot),(205,arrowBot)])
        screen.blit( textBitmap, (160,220) )

        motorSpeedR = motorPowerR
        textBitmap = font.render("{}%".format(motorSpeedR), True, RED )
        arrowLength = 20 + abs(motorSpeedR * 2)
        arrowTop = 230-(arrowLength/2)
        pygame.draw.rect(screen, PURPLE, pygame.Rect(620,230-(arrowLength/2),30,arrowLength))
        if motorSpeedR < 0:
            pygame.draw.polygon(screen, PURPLE, [(635,arrowTop-30),(605,arrowTop),(665,arrowTop)])
        elif motorSpeedR > 0:
            arrowBot = arrowTop + arrowLength
            pygame.draw.polygon(screen, PURPLE, [(635,arrowBot+30),(605,arrowBot),(665,arrowBot)])
        screen.blit( textBitmap, (620,220) )
    else:
        print("Unable to draw robot when screen is not initialised in pygame.")
        

def drawRotatedRectangle(screen,x,y,w,h,rot,colour):
    GREEN = [0,255,0]
    # define a surface (rectangle) which can be transformed  
    image1 = pygame.Surface((w, h))  
    # set colour to be transparent background for rotating an image  
    image1.set_colorkey(GREEN)  
    # fill the rectangle / surface with solid color  
    image1.fill(colour)  
    # transform the orignal image (-rot to +ve rotation is clockwise)
    image2 = pygame.transform.rotate(image1 , -rot)  
    rect = image2.get_rect()  
    # set the centre position of rotated rectangle to the desired position  
    rect.center = (x, y)  
    # drawing the rotated rectangle to the screen  
    screen.blit(image2 , rect)
    
    
def displayError(message):
    screen = pygame.display.get_surface()
    screen.fill( (0,0,0) )
    font = pygame.font.Font(None, 32)
    textBitmap = font.render(message, True, [255,0,0] )
    screen.blit( textBitmap, (20, 200) )
    
    
def main():
    """ Test function for servos and motors
    """
    sb.pulseWatchdog()

    """
    setSteeringFrontLeft(130) #44
    sb.watchdogPause(1)
    setSteeringFrontRight(130) #40
    sb.watchdogPause(1)
    setSteeringRearLeft(130) #41
    sb.watchdogPause(1)
    setSteeringRearRight(130) #40
    sb.watchdogPause(1)
    setSteeringStraight()
    sb.watchdogPause(1)
    setLeftMotorPower(30)
    sb.watchdogPause(1)
    setLeftMotorPower(-30)
    sb.watchdogPause(1)
    setLeftMotorPower(0)
    setRightMotorPower(30)
    sb.watchdogPause(1)
    setRightMotorPower(-30)
    sb.watchdogPause(1)
    setRightMotorPower(0)
    """
    setSteering(0)
    speed = 50
    setLeftMotorPower(speed)
    setRightMotorPower(speed)
    sb.watchdogPause(1)
    stopAll()    
    sb.watchdogPause(0.25)
    speed = -50
    setLeftMotorPower(speed)
    setRightMotorPower(speed)
    sb.watchdogPause(1)
    
    stopAll()    
    
if __name__ == '__main__':
    main()
