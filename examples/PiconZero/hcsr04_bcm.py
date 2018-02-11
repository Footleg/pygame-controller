#======================================================================
#
# Python Module to handle an HC-SR04 Ultrasonic Module on a single Pin
# Aimed at use on Picon Zero
#
# Created by Gareth Davies, Mar 2016
# Copyright 4tronix
#
# Modified by Footleg, Feb 2018
# Changed to use GPIO.BCM mode so it can be used with the Blinkt
# library from Pimoroni.
# Added signal cleaning function to get cleaner reading of distance.
#
# This code is in the public domain and may be freely copied and used
# No warranty is provided or implied
#
#======================================================================

import RPi.GPIO as GPIO, sys, threading, time, os, subprocess


# Define Sonar Pin (BCM numbering) (Uses same pin for both Ping and Echo)
sonar = 20

#======================================================================
# General Functions
#
def init():
    """ Initialise GPIO in BCM pin numbering mode) """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def cleanup():
    """ Clean up GPIO """
    GPIO.cleanup()

#======================================================================

#======================================================================
# UltraSonic Functions
#
def getDistance():
    """ Returns the distance in cm to the nearest reflecting object. 0 == no object """
    GPIO.setup(sonar, GPIO.OUT)
    # Send 10us pulse to trigger
    GPIO.output(sonar, True)
    time.sleep(0.00001)
    GPIO.output(sonar, False)
    start = time.time()
    count=time.time()
    GPIO.setup(sonar,GPIO.IN)
    while GPIO.input(sonar)==0 and time.time()-count<0.1:
        start = time.time()
    count=time.time()
    stop=count
    while GPIO.input(sonar)==1 and time.time()-count<0.1:
        stop = time.time()
    # Calculate pulse length
    elapsed = stop-start
    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34000
    # That was the distance there and back so halve the value
    distance = distance / 2
    return distance

#======================================================================

#======================================================================
# Data processing/signal clean up functions
#
def getDistanceClean(count = 5, threshold = 800, maxTime = 0.3, debug=False):
    """ Returns the distance in cm to the nearest reflecting object.
        This function takes several readings and ignores outliers to
        give a more stable measurement.
        Returns -1 if no reflected signal was detected (i.e. no obstructions).        
    """
    readings = []
    nopings = 0
    start = time.time()
    for i in range(count):
        measure = getDistance()
        if measure < threshold:
            readings.append( round(measure, 1) )
        else:
            nopings += 1
        if time.time() - start > maxTime:
            break

    if debug:
        print("Readings {}; Non-readings={}".format(readings,nopings) )

    readCount = len(readings)
    if readCount == 0:
        return -1
    elif readCount == 1:
        return readings[0]
    elif readCount == 2:
        return round((readings[0] + readings[1])/2,1)
    else:
        #Remove outliers (keep readings within 10% of middle value)
        readings.sort()
        mid = readings[ int(readCount / 2) - 1 ]
        kept = 0
        sumKept = 0
        keep = []
        for i in range(readCount):
            if abs(readings[i] - mid)/mid < 0.1:
                keep.append(readings[i])
                kept += 1
                sumKept += readings[i]
                
        if debug:
            print("Kept vals {}".format(keep) )
            
        #Return average of kept readings
        return round((sumKept/kept),1)
    
def test():
    init()
    for i in range(100):
        start = time.time()
        print("DistanceClean returned: {}".format( getDistanceClean(5,800,0.3,True) ) )
        end = time.time()
        print("Sample took: {}".format( end - start ) )
        
        time.sleep(1)
    cleanup()

if __name__ == '__main__':
    test()
