#!/usr/bin/python

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
import time

# Initialise the i2c bus to communicate with devices
i2c = busio.I2C(SCL, SDA)

# Initialise the PWM device using the default address
pwm = PCA9685(i2c)
    
# Set frequency of PWM pulses (default is 50 Hz)
freqPWM = 50
pwm.frequency = freqPWM                        

#Define the channels which the servos are connected to
turnChannel = 0
fwdChannel = 1
liftChannel = 2
jawsChannel = 3

#Define the minimum and maximum positions the servos can move between safely
turnMin = 10  #Right
turnMax = 178 #Left

fwdMin = 80  #Back
fwdMax = 180 #Forward

liftMin = 40  #Down
liftMax = 160 #Up

jawsMin = 30  #Open
jawsMax = 170 #Closed

def setServoPosition(channel, position):
    """ Function which sets the position of a servo in degrees
    """
    servoMin = 105  #105 Min pulse length out of 4096
    servoMax = 475  #500 Max pulse length out of 4096
    
    #Convert position in degrees to value in range min-max
    pulse = int( ( (servoMax - servoMin) * position / 180 ) + servoMin)
    
    if (pulse < servoMin) or (pulse > servoMax):
        print("Calculated servo pulse {} is outside supported range of {} to {}".format(pulse,servoMin,servoMax) )
    else:
        # print("Setting servo {} pulse to {}".format(channel,pulse) )
        active_channel = pwm.channels[channel]
        active_channel.duty_cycle = pulse
    
    
def setArmPosition(channel, position):
    """ Function which sets the position of a servo in degrees
        with safetly checking to prevent servos being moved outside of their
        safe moving range when connected to the MeArm
    """

    safeMin = 90
    safeMax = 90
    servoName = ""
    
    if channel == turnChannel :
        safeMin = turnMin
        safeMax = turnMax
        servoName = "Base Rotation"
    elif channel == fwdChannel :
        safeMin = fwdMin
        safeMax = fwdMax
        servoName = "Forward Reach"
    elif channel == liftChannel :
        safeMin = liftMin
        safeMax = liftMax
        servoName = "Arm Height"
    elif channel == jawsChannel :
        safeMin = jawsMin
        safeMax = jawsMax
        servoName = "Jaws"
    
    if safeMin <= position <= safeMax :
        setServoPosition(channel, position)
    else:
        print("Position {} outside of safe range of {} to {} for {} servo".format(position, safeMin, safeMax, servoName) )
        
def main():
    # ===========================================================================
    # Test Servos minimum and maximum positions
    # ===========================================================================
    for i in range(0,4):
        min = 80
        max = 100
        
        if i == 3:
            min = jawsMin
            max = jawsMax
        setArmPosition(i, min)
        time.sleep(1)
        setArmPosition(i, max)
        time.sleep(1)

    #All together
    for i in range(0,4):
        setArmPosition(i,80)
    
    time.sleep(1)

    for i in range(0,4):
        setArmPosition(i,130)

    time.sleep(1)
    #Set all servos to middle position
    for i in range(0,4):
        setArmPosition(i,90)
    
    setArmPosition(3,165)
    time.sleep(1)


if __name__ == '__main__':
    main()
