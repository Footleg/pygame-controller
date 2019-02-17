#!/usr/bin/env python3

import sys
sys.path.append('./../../')
sys.path.append('/home/pi/4tronix/robohat')

import pygame, random, time, math
from PygameController import RobotController
import robohat

#Initialise global variables
power = 0
turn = 0
minMovingSpeed = 30
message = ""

#Multiplier applied to speed so top speed is set when stick is not quite at maximum position
speedFactor = 1.1


def motorSpeed(ls,rs):
    global message
    lm = 0
    rm = 0    
    if ls == 0 :
        """
        if rs == 0 :
            lm = 0
            rm = 0
        elif rs < 0 :
            lm = rs * 100
            rm = -lm
        else rs > 0 :
            lm = rs * 100
            rm = -lm
        """
        lm = rs * 100
        rm = -lm

    elif rs == 0 :
        if ls < 0 :
            lm = -ls * 100
            rm = lm
        else :
            lm = -ls * 100
            rm = lm
    elif rs < 0 :
        if ls < 0 :
            lm = 0
            rm = -ls * 100
        elif ls > 0 :
            lm = 0    
            rm = -ls * 100
    else :
        if ls < 0 :
            lm = -ls * 100
            rm = 0
        elif ls > 0 :
            lm = -ls * 100
            rm = 0
            
    message = message + "  lm = {}, rm = {}".format( int(lm), int(rm) )
    
    #set the power for each motor
    robohat.setMotorsPower(lm,rm)


def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format( status ) )
            

def leftStickChangeHandler(valLR, valUD):
    """Handler function for left analogue stick"""
    global power
    power = valUD


def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global turn
    turn = valLR


def main():
    global message
    ## Check that required hardware is connected ##

    #Initialise the controller board
    robohat.init()
   
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Lego Robohat Robot", initStatus,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler)
        
        if cnt.initialised : 
            keepRunning = True
            #Indicate success here, we are ready to run
            print (' yippee!!!!!')
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            cnt.message = message
            
           
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
            
            message = "Power={0:.2f}, Turn={0:.2f}".format(power,turn)
            motorSpeed(power, turn)
    finally:
        #Clean up and turn off Blinkt LEDs
        robohat.cleanup()
        pygame.quit()


if __name__ == '__main__':
    main()
