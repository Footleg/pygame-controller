#!/usr/bin/env python3

import sys
sys.path.append('./../../')
sys.path.append('/home/pi/4tronix/piconzero/')

import pygame, random, time, math
from PygameController import RobotController
import piconzero3 as pz

#Initialise lobal variables
speed = 0
minMovingSpeed = 30
message = ""

#Multiplier applied to speed so top speed is set when stick is not quite at maximum position
speedFactor = 1.1

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

    global steering
    steering = int(right_limit - ( (valLR + 1) * (right_limit - left_limit) / 2 ) )
    pz.setOutput (servo_no, steering)


def leftStickChangeHandlerV2(valLR, valUD):
    """Handler function for left analogue stick"""
    mode = "Drive: "
    
    fwdpower = -valUD
    turnpower = abs(valLR)
    
    if (fwdpower == 0) and (turnpower == 0):
        mode = "Stop: "
        speedR = 0
        speedL = 0
    elif abs(fwdpower) < 0.2 :
        #Spin only, apply at max half power
        speedR = int( valLR * 64 )
        speedL = -speedR
        mode = "Spin: "
    else:    
        #Start by applying forward/reverse power to both tracks equally
        speedL = int( fwdpower * 128 )
        speedR = speedL


    global message
    message = mode + " Speed L: {}, Speed R: {}".format( speedL, speedR ) 
        
    #Set motor speeds
    pz.setMotor(0, speedL)
    pz.setMotor(1, speedR)


def main():
    global message
    ## Check that required hardware is connected ##

    #Initialise the controller board
    pz.init()

    #Confirm board detected
    vsn = pz.getRevision()
    if (vsn[1] == 2):
        print("Board Type:", "Picon Zero")
    else:
        print("Board Type:", vsn[1])
    print("Firmware version:", vsn[0])

    # Define which inputs and outputs are configured
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Lego Picon Zero Robot", initStatus,
                              leftStickChanged = leftStickChangeHandlerV2)
        
        if cnt.initialised :
            keepRunning = True
            #Indicate success here, we are ready to run
            pz.forward(50)
            time.sleep(0.25)
            pz.stop()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            cnt.message = message
            
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
    
    finally:
        #Clean up and turn off Blinkt LEDs
        pz.stop()
        pz.cleanup()
        pygame.quit()


if __name__ == '__main__':
    main()
