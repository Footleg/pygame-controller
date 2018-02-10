#!/usr/bin/python

import MeArmServoControl as arm
from ../../PygameController import RobotController
import pygame
import blinkt as blkt


#Declare variables to hold servo positions
posBase = ((arm.turnMax - arm.turnMin)/2) + arm.turnMin
posLift = ((arm.liftMax - arm.liftMin)/2) + arm.liftMin
posReach = ((arm.fwdMax - arm.fwdMin)/2) + arm.fwdMin
posJaws = arm.jawsMin
turnValue = 0
turnSpeed = 3

def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
        blkt.set_all(0,0,255)
    elif status < 0 :
        print("No supported controller detected")
        blkt.set_all(255,0,0)
    else:
        print("Waiting for controller {}".format(status) )
        if status < 9 :
            blkt.set_pixel(status-1,255,128,0)
        elif status < 17 :
            blkt.set_pixel(status-9,255,50,0)

    blkt.show()


def leftTriggerChangeHandler(val):
    """Handler function for left analogue trigger"""
    global posJaws
    posJaws = ( ( (-val+1) / 2) * ( arm.jawsMax - arm.jawsMin ) ) + arm.jawsMin
    arm.setArmPosition ( arm.jawsChannel, posJaws )


def rightTriggerChangeHandler(val):
    """Handler function for right analogue trigger"""
    
    
def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global posLift
    posLift = ( ( (-valUD+1) / 2) * ( arm.liftMax - arm.liftMin ) ) + arm.liftMin
    arm.setArmPosition ( arm.liftChannel, posLift )

    
def leftStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global posReach
    posReach = ( ( (-valUD+1) / 2) * ( arm.fwdMax - arm.fwdMin ) ) + arm.fwdMin
    arm.setArmPosition ( arm.fwdChannel, posReach )
 
 
def hatChangeHandler(valUD, valLR):
    """Handler function for hat"""
    global turnValue
    turnValue = -valLR


def turnLeft(valLR):
    global turnValue
    turnValue = valLR


def turnRight(valLR):
    global turnValue
    turnValue = -valLR


def main():
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    global posBase
    global turnValue
    
    try:
        cnt = RobotController("Servo and Blinkt Controller", initStatus,
                              leftTriggerChanged = leftTriggerChangeHandler,
                              rightTriggerChanged = rightTriggerChangeHandler,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler,
                              hatChanged = hatChangeHandler,
                              leftBtn1Changed = turnLeft,
                              rightBtn1Changed = turnRight
                              )

        if cnt.initialised :
            keepRunning = True
            blkt.set_all(0,255,0)
            blkt.show()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
            if turnValue != 0 :
                newBase = posBase + (turnValue * turnSpeed)
                if arm.turnMin <= newBase <= arm.turnMax :
                    posBase = newBase
                    arm.setArmPosition ( arm.turnChannel, posBase )


    finally:
        #Clean up and turn off Blinkt LEDs
        pygame.quit()
        if cnt.initialised :
            blkt.clear()
            blkt.show()

if __name__ == '__main__':
    main()
    