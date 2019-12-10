#!/usr/bin/env python3
import sys,time
from Adafruit_PWM_Servo_Driver import PWM
from Adafruit_MCP230xx import Adafruit_MCP230XX

# PWM board configuration values.
freqPWM = 50    #Frequency of PWM pulses (default is 50 Hz)
#Set servo min and max pulse length for the range of rotation of the servo model being used
servoMin = 105  #105 Min pulse length (out of 4096)
servoMax = 475  #500 Max pulse length (out of 4096)
servoRange = 180 #Rotation range in degrees of the servos being used
motorPowerLimiting = 50 #Default limits motors to 50 power
maxPulseLength = 4090 #Length of an always on pulse for the pwm board (cap below true max of 4096 as pwm cuts out at this pulse length)
channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Store pulse lengths sent to each channel (for debug info)
motorAChannel1 = 12
motorAChannel2 = 13
motorBChannel1 = 15
motorBChannel2 = 14


# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)

# Set frequency to 50 Hz
pwm.setPWMFreq(freqPWM)

# Initialise MCP 16 channel io
mcp = Adafruit_MCP230XX(address = 0x20, num_gpios = 16)

def setServoPosition(channel, position):
    """ Sets the position of a servo in degrees
    """
    global channelPulseLengths

    #Convert position in degrees to value in range min-max
    pulse = int( ( (servoMax - servoMin) * position / servoRange ) + servoMin)

    if (pulse < servoMin) or (pulse > servoMax):
        print("Calculated servo pulse {} is outside supported range of {} to {}".format(pulse,servoMin,servoMax) )
    else:
        # print("Setting servo {} pulse to {}".format(channel,pulse) )
        pwm.setPWM(channel, 0, pulse)
        channelPulseLengths[channel] = pulse


def setMotorPowerLimiting(percentage):
    """ Sets limit to maximum motor power (as a percentage of motor board input voltage)
        Used to limit the maximum voltage the motors receive via PWM limiting.
        e.g. Setting this to 50% will mean when the motor percent on method is sent a value
        of 100%, the motors will only actually be send a PWM pulse which is on 50% of the time.
    """
    global motorPowerLimiting

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

    #Scale down fully on pulse using percentage power limiting global variable value
    maxPulse = maxPulseLength * motorPowerLimiting / 100

    #Convert percentage to pulse length
    pulse = int( percent * maxPulse / 100 )

    #Limit pulse length to between zero and maximum
    if (percent < 0):
        pulse = 0
    elif (percent > 100):
        pulse = maxPulse

    #print("Setting servo {} pulse to {}".format(channel,pulse) )
    pwm.setPWM(channel, 0, pulse)
    channelPulseLengths[channel] = pulse


def setConstantOn(channel):
    """ Sets a channel to completely on (for logical high).
    """
    pwm.setPWM(channel, 0, maxPulseLength)
    channelPulseLengths[channel] = maxPulseLength


def allOff():
    """ Sets all outputs off """
    global channelPulseLengths

    pwm.setAllPWM(0,0)
    channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def main():
    """ Test function for servos and motors
    """

    """
    #Servo on channel 0
    testChannel = 0
    print("Setting servo on channel {} to 0 degrees position.".format(testChannel))
    setServoPosition(testChannel, 0)
    time.sleep(1)
    print("Setting servo on channel {} to 180 degrees position.".format(testChannel))
    setServoPosition(testChannel, 180)
    time.sleep(1)
    print("Setting servo on channel {} to 90 degrees position.".format(testChannel))
    setServoPosition(testChannel, 90)
    time.sleep(1)
    
    #Motor A
    print("Setting motor A to power 50 forwards.")
    setPercentageOn(motorAChannel1,0)
    setPercentageOn(motorAChannel2,50)
    time.sleep(2)
    print("Setting motor A to power 0.")
    setPercentageOn(motorAChannel2,0)
    time.sleep(1)
    print("Setting motor A to power 50 reverse.")
    setPercentageOn(motorAChannel1,50)
    time.sleep(2)
    print("Setting motor A to power 0.")
    setPercentageOn(motorAChannel1,0)
    
    #Motor B
    print("Setting motor B to power 50 forwards.")
    setPercentageOn(motorBChannel1,0)
    setPercentageOn(motorBChannel2,50)
    time.sleep(2)
    print("Setting motor B to power 0.")
    setPercentageOn(motorBChannel2,0)
    time.sleep(1)
    print("Setting motor B to power 50 reverse.")
    setPercentageOn(motorBChannel1,50)
    time.sleep(2)
    print("Setting motor B to power 0.")
    setPercentageOn(motorBChannel1,0)
    """
    
    #Test one PWM output
    setConstantOn(11)
    time.sleep(2)
    
    #Test one IO
    ioPin = 15
    mcp.config(ioPin, mcp.OUTPUT)
    mcp.output(ioPin, 1)  # Pin High
    time.sleep(2);
    mcp.output(ioPin, 0)  # Pin Low

    
    #All Off
    print("Turning off all channels.")
    allOff()


if __name__ == '__main__':
    main()