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
import pygame
import RobotControl as rc

#Set servo min and max pulse length for the range of rotation of the servo model being used
servoMin = 105  #105 Min pulse length (out of 4096)
servoMax = 475  #500 Max pulse length (out of 4096)
servoRange = 180 #Rotation range in degrees of the servos being used
motorPowerLimiting = 50 #Default limits motors to 50 power
channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Store pulse lengths sent to each channel (for debug info)

#Virtual hardware channels for mock robot
servoChFL = 0
servoChFR = 1
servoChBL = 2
servoChBR = 3
motorChL1 = 12
motorChL2 = 13
motorChR1 = 14
motorChR2 = 15

#Globals to store positions of servos and motor channel percentage on
motorChPctOnL1 = 0
motorChPctOnR1 = 0
motorChPctOnL2 = 0
motorChPctOnR2 = 0
servoPosFL = 0
servoPosFR = 0
servoPosBL = 0
servoPosBR = 0


def setServoPosition(channel, position):
    """ Sets the position of a servo in degrees
    """
    global channelPulseLengths, servoPosFL, servoPosFR, servoPosBL, servoPosBR
    
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
        
        print("ChL1:{},ChL2:{}".format(motorChPctOnL1,motorChPctOnL2) )

        if validChannel:
            drawVirtualRobot( pygame.display.get_surface() )
            channelPulseLengths[channel] = pulse

    
def setMotorPowerLimiting(percentage):
    """ Sets limit to maximum motor power (as a percentage of motor board input voltage)
        Used to limit the maximum voltage the motors receive via PWM limiting.
        e.g. Setting this to 50% will mean when the motor percent on method is sent a value
        of 100%, the motors will only actually be send a PWM pulse which is on 50% of the time.
    """
    global motorPowerLimiting
    
    print("Setting power limiting to {}".format(percentage) )
    if percentage > 0:
        if percentage > 100:
            motorPowerLimiting = 100
        else:
            motorPowerLimiting = percentage
    else:
        motorPowerLimiting = 0

    
def setPercentageOn(channel, percent):
    """ Sets the percentage of time a channel is on per cycle.
        For use with PWM motor speed control.
    """
    global channelPulseLengths, motorChPctOnL1, motorChPctOnR1, motorChPctOnL2, motorChPctOnR2

    #Fully on pulse length is 4096.
    #Limit to percentage of this using motorPowerLimiting value
    maxPulse = 4096 * motorPowerLimiting / 100
    
    #Convert percentage to pulse length
    pulse = int( percent * maxPulse / 100 )
    
    #Limit pulse length to between zero and maximum
    if (percent < 0):
        pulse = 0
    elif (percent > 100):
        pulse = maxPulse

    #Now set actual percentage on calculated from pulse length which would be send to real hardware
    percentOn = int(pulse * 100 / 4096)
    
    print("Motor channel {} requested power: {}, limited to {} by power limiting setting".format(channel, percent, percentOn) )
    validChannel = True
    if channel == motorChL1:
        motorChPctOnL1 = percentOn
    elif channel == motorChR1:
        motorChPctOnR1 = percentOn
    elif channel == motorChL2:
        motorChPctOnL2 = percentOn
    elif channel == motorChR2:
        motorChPctOnR2 = percentOn
    else:
        validChannel = False
        displayError("Call to set servo position on channel {} which has no servo attached.".format(channel))
    
    if validChannel:
        drawVirtualRobot( pygame.display.get_surface() )
        channelPulseLengths[channel] = pulse
        
    
def allOff():
    """ Sets all outputs off """
    global channelPulseLengths
    
    channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    
def drawVirtualRobot(screen):
    """ Draw graphical representation of robot on screen, indicating wheel positions and motor speeds """
    
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
    drawRotatedRectangle(screen,WHEEL_L_X,WHEEL_B_Y,WHEEL_W,WHEEL_H,90-servoPosBL+rc.servoRearLeftOffset,BLACK)
    pygame.draw.circle(screen, RED,(WHEEL_L_X,WHEEL_B_Y),CIRCLE_DIA)
    drawRotatedRectangle(screen,WHEEL_R_X,WHEEL_B_Y,WHEEL_W,WHEEL_H,90-servoPosBR+rc.servoRearRightOffset,BLACK)
    pygame.draw.circle(screen, RED,(WHEEL_R_X,WHEEL_B_Y),CIRCLE_DIA)
    drawRotatedRectangle(screen,WHEEL_L_X,WHEEL_F_Y,WHEEL_W,WHEEL_H,90-servoPosFL+rc.servoFrontLeftOffset,BLACK)
    pygame.draw.circle(screen, RED,(WHEEL_L_X,WHEEL_F_Y),CIRCLE_DIA)
    drawRotatedRectangle(screen,WHEEL_R_X,WHEEL_F_Y,WHEEL_W,WHEEL_H,90-servoPosFR+rc.servoFrontRightOffset,BLACK)
    pygame.draw.circle(screen, RED,(WHEEL_R_X,WHEEL_F_Y),CIRCLE_DIA)
    
    #Display motor speeds
    font = pygame.font.Font(None, 28)
    motorSpeedL = motorChPctOnL2 - motorChPctOnL1
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

    motorSpeedR = motorChPctOnR2 - motorChPctOnR1
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
    """ Test function for module
    """
    print("""This module cannot run stand alone. Use it from within a pygame application where
the screen has been initialised.""")
  
    
if __name__ == '__main__':
    main()