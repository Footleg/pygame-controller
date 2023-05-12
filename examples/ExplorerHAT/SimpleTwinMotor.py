#!/usr/bin/env python3
""" Example of a robot using tank steering with two motors for left and right tracks.
    This robot uses the Explorerhat Pro board from Pimoroni. The speed and steering are
    controlled from the left and right sticks respectively, so in this example the
    change handler functions store the stick postions in variables and these are
    used to update the motor powers in the main program loop. (See the PiconZero
    Simple Twin Motor example for an alternative way to control a robot with just a
    single stick for both power and steering).
"""
import pygame, random, time, math
from pygamecontroller import RobotController
import explorerhat

#Initialise global variables
power = 0
turn = 0
minMovingSpeed = 30
message = ""

#Multiplier applied to speed so top speed is set when stick is not quite at maximum position
speedFactor = 1.1
stickDeadzone = 0.05

def motorSpeed(ls,rs):
    global message
    lm = 0
    rm = 0    
    if -stickDeadzone < ls < stickDeadzone :
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

    elif rs < -stickDeadzone :
        if ls < -stickDeadzone :
            lm = 0
            rm = -ls * 100
        elif ls > stickDeadzone :
            lm = 0    
            rm = -ls * 100
    elif rs > stickDeadzone :
        if ls < -stickDeadzone :
            lm = -ls * 100
            rm = 0
        elif ls > stickDeadzone :
            lm = -ls * 100
            rm = 0
    else:
        if ls < -stickDeadzone :
            lm = -ls * 100
            rm = lm
        else :
            lm = -ls * 100
            rm = lm
            
    message = message + "  lm = {}, rm = {}".format( int(lm), int(rm) )
    print(message)
    
    #set the power for each motor
    explorerhat.motor.one.speed(int(lm))
    explorerhat.motor.two.speed(int(rm))


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
    
   
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("ExplorerHAT Robot", initStatus,
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
        explorerhat.motor.one.stop()
        explorerhat.motor.two.stop()
        pygame.quit()


if __name__ == '__main__':
    main()
