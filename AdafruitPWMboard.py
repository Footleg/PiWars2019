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

#Set servo min and max pulse length for the range of rotation of the servo model being used
servoMin = 105  #105 Min pulse length (out of 4096)
servoMax = 475  #500 Max pulse length (out of 4096)
servoRange = 180 #Rotation range in degrees of the servos being used
motorPowerLimiting = 50 #Default limits motors to 50 power
channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Store pulse lengths sent to each channel (for debug info)


def setServoPosition(channel, position):
    """ Sets the position of a servo in degrees
    """
    global channelPulseLengths
    
    #Convert position in degrees to value in range min-max
    pulse = int( ( (servoMax - servoMin) * position / servoRange ) + servoMin)
    
    if (pulse < servoMin) or (pulse > servoMax):
        print("Calculated servo pulse {} is outside supported range of {} to {}".format(pulse,servoMin,servoMax) )
    else:
        #print("Setting servo {} pulse to {}".format(channel,pulse) )
        #pwm.setPWM(channel, 0, pulse)
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
    global channelPulseLengths
    
    #Fully on pulse length is 4096.
    #Scale this down using percentage power limiting global variable value
    maxPulse = 4096 * motorPowerLimiting / 100
    
    #Convert percentage to pulse length
    pulse = int( percent * maxPulse / 100 )
    
    #Limit pulse length to between zero and maximum
    if (percent < 0):
        pulse = 0
    elif (percent > 100):
        pulse = maxPulse

    #pwm.setPWM(channel, 0, pulse)
    channelPulseLengths[channel] = pulse

    ### Code for virtual robot representation below this line ###
    
    #Calculate actual percentage on from pulse length which would be sent to real hardware
    percentOn = int(pulse * 100 / 4096)
    print("Motor channel {} requested power: {}, limited to {} by power limiting setting".format(channel, percent, percentOn) )
        
    
def allOff():
    """ Sets all outputs off """
    global channelPulseLengths
    
    channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    
def main():
    """ Test function for module
    """
    print("""This module cannot run stand alone. Use it from within a pygame application where
the screen has been initialised.""")
  
    
if __name__ == '__main__':
    main()