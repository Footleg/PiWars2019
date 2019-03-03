#!/usr/bin/env python3
import sys,time
sys.path.append('/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver/')

from Adafruit_PWM_Servo_Driver import PWM

# PWM board configuration values. 
freqPWM = 50    #Frequency of PWM pulses (default is 50 Hz)
#Set servo min and max pulse length for the range of rotation of the servo model being used
servoMin = 105  #105 Min pulse length (out of 4096)
servoMax = 475  #500 Max pulse length (out of 4096)
servoRange = 180 #Rotation range in degrees of the servos being used
motorPowerLimiting = 50 #Default limits motors to 50 power
channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Store pulse lengths sent to each channel (for debug info)

# Initialise the PWM device using the default address
pwm = PWM(0x40, debug=False)
    
# Set frequency to 50 Hz 
pwm.setPWMFreq(freqPWM)


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

    #print("Setting servo {} pulse to {}".format(channel,pulse) )
    pwm.setPWM(channel, 0, pulse)
    channelPulseLengths[channel] = pulse
      
    
def allOff():
    """ Sets all outputs off """
    global channelPulseLengths
    
    pwm.setAllPWM(0,0)
    channelPulseLengths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    
def main():
    """ Test function for servo
    """
    testChannel = 0
    print("Setting servo on channel {} to 0 degrees position.".format(testChannel))
    setServoPosition(testChannel, 0);
    time.sleep(1)
    print("Setting servo on channel {} to 180 degrees position.".format(testChannel))
    setServoPosition(testChannel, 180);
    time.sleep(1)
    print("Setting servo on channel {} to 90 degrees position.".format(testChannel))
    setServoPosition(testChannel, 90);
    time.sleep(1)
    
    
if __name__ == '__main__':
    main()