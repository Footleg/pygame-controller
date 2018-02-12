#!/usr/bin/env python3

import sys
sys.path.append('./../../')
sys.path.append('./../Blinkt/')
sys.path.append('/home/pi/piconzero/')

import pygame, random, time, math
import blinkt as blkt
from PygameController import RobotController
from BlinktController import initStatus, showIP
import piconzero3 as pz
import hcsr04_bcm as hcsr04

#Global variables
message = ""


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
        
        if turnpower > 0.0 :
            #Reduce speed of one track compared to powered speed of other
            speedReduction = int( fwdpower * turnpower * 128 )
                
            #Remove turn power from one track only
            if valLR < 0.0 :
                speedR -= speedReduction
            else:
                speedL -= speedReduction

    global message
    message = mode + " Speed L: {}, Speed R: {}".format( speedL, speedR ) 
    
    #Set LEDs based on motor speeds
    colR = 0
    colG = 0
    colB = 0
    if speedL > 0:
        colR = speedL
    else:
        colG = -speedL
        
    if speedR > 0:
        colB = speedR
    elif speedL > 0:
        colG = -speedR
    else:
        colR = -speedR
    
    blkt.clear()
    for i in range( 0, int( (abs(speedL) + abs(speedR)) * 8 / 250 ) ):
        if ( (speedL + speedR) < 0 ) or ( (speedL == -speedR) and (speedL > 0) ):
            idx = 7 - i
        else:
            idx = i
        blkt.set_pixel(idx,colR,colG,colB)
    blkt.show()
        
    #Set motor speeds
    pz.setMotor(0, speedL)
    pz.setMotor(1, speedR)


def startBtnHandler(btnState):
    if btnState == 1:
        showIP()
    
def main():
    global message
    
    ## Check that required hardware is connected ##

    #Initialise the controller board
    pz.init()
    hcsr04.init()

    #Confirm board detected
    vsn = pz.getRevision()
    if (vsn[1] == 2):
        print("Board Type:", "Picon Zero")
    else:
        print("Board Type:", vsn[1])
    print("Firmware version:", vsn[0])

    # Define which inputs and outputs are configured
    ## servo_no = 0
    
    # Set output modes of any Picon Zero outputs
    ##
    
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Zumo Robot with Blinkt", initStatus,
                              leftStickChanged = leftStickChangeHandlerV2,
                              startBtnChanged = startBtnHandler)
        
        if cnt.initialised :
            keepRunning = True
            blkt.set_all(0,255,0)
            blkt.show()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            cnt.message = message
            
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
            
            #Measure distance
            testDist = hcsr04.getDistanceClean()
            if testDist > 0 :
                distance = testDist
            else:
                distance = 1000
                
            message = "Distance {}".format(distance)
    
    finally:
        #Clean up and turn off Blinkt LEDs
        pz.stop()
        pz.cleanup()
        blkt.clear()
        blkt.show()
        hcsr04.cleanup()
        pygame.quit()


if __name__ == '__main__':
    main()
