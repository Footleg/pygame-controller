#!/usr/bin/python
""" This example uses the Adafruit 16-Channel 12-bit PWM/Servo HAT to control a
    Mime Industries MeArm (a low cost robot arm kit). The servo positions are
    controlled using a game controller and the code limits the range of the servos
    to prevent them trying to move beyond positions the robot arm constrains them to.
    
    The Adafruit HAT is controlled using the Blinka library and circuit python
    adafruit_pca9685 module. These dependencies can be installed/upgraded using
    the following installation command:
    
    pip3 install --upgrade RPI.GPIO adafruit_blinka adafruit-circuitpython-pca9685
"""
import pygame
from pygamecontroller import RobotController
import MeArmServoControl as arm


#Declare variables to hold servo positions
posBase = 0
posLift = 0
posReach = 0
posJaws = 0

#Variables to hold values to control change in position of each servo
turnValue = 0
turnSpeed = 3
liftChange = 0
liftSpeed = 4
reachChange = 0
reachSpeed = 4
jawsChange = 0
jawsSpeed = 5

#Control modes map the controller in different ways to the servos
controlMode = 1


def resetArm():
    global posBase, posReach, posLift, posJaws
    
    posBase = ((arm.turnMax - arm.turnMin)/2) + arm.turnMin
    posLift = ((arm.liftMax - arm.liftMin)*1/4) + arm.liftMin
    posReach = ((arm.fwdMax - arm.fwdMin)*1/4) + arm.fwdMin
    posJaws = arm.jawsMax
    
    arm.setArmPosition ( arm.jawsChannel, posJaws )
    arm.setArmPosition ( arm.liftChannel, posLift )
    arm.setArmPosition ( arm.fwdChannel, posReach )
    arm.setArmPosition ( arm.turnChannel, posBase )
    

def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
    elif status < 0 :
        print("No supported controller detected")
    else:
        print("Waiting for controller {}".format(status) )
        if status % 2 > 0:
            arm.setArmPosition ( arm.jawsChannel, arm.jawsMax )
        else:
            arm.setArmPosition ( arm.jawsChannel, arm.jawsMax - 20)
            
        
def leftTriggerChangeHandler(val):
    """ Handler function for left analogue trigger:
        Controls the MeArm jaws
    """
    global posJaws
    posJaws = ( ( (-val+1) / 2) * ( arm.jawsMax - arm.jawsMin ) ) + arm.jawsMin
    arm.setArmPosition ( arm.jawsChannel, posJaws )


def rightTriggerChangeHandler(val):
    """Handler function for right analogue trigger"""
    leftTriggerChangeHandler(val)
    
    
def leftStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global posReach, reachChange
    #global turnValue
    
    if controlMode == 0:
        posReach = ( ( (-valUD+1) / 2) * ( arm.fwdMax - arm.fwdMin ) ) + arm.fwdMin
        arm.setArmPosition ( arm.fwdChannel, posReach )
    else:
        #turnValue = -valLR
        reachChange = -valUD
        
    
def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global posLift, liftChange
    
    if controlMode == 0:
        posLift = ( ( (-valUD+1) / 2) * ( arm.liftMax - arm.liftMin ) ) + arm.liftMin
        arm.setArmPosition ( arm.liftChannel, posLift )
    else:
        liftChange = -valUD


def hatChangeHandler(valLR, valUD):
    """Handler function for hat"""
    global turnValue
    global jawsChange
    turnValue = -valLR
    jawsChange = -valUD


def turnLeft(val):
    global turnValue
    turnValue = val


def turnRight(val):
    global turnValue
    turnValue = -val


def toggleMode(val):
    global controlMode
    
    if val == 1:
        if controlMode == 0:
            controlMode = 1
        else:
            controlMode = 0
    

def main():
    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    global posBase, turnValue, posJaws, jawsChange, posReach, posLift
    
    try:
        cnt = RobotController("MeArm Controller", initStatus,
                              leftTriggerChanged = leftTriggerChangeHandler,
                              rightTriggerChanged = rightTriggerChangeHandler,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler,
                              hatChanged = hatChangeHandler,
                              leftBtn1Changed = turnLeft,
                              rightBtn1Changed = turnRight,
                              triangleBtnChanged = toggleMode
                              )

        if cnt.initialised :
            keepRunning = True
            resetArm()
        else:
            keepRunning = False
            
        # -------- Main Program Loop -----------
        while keepRunning == True :
            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()
            message = "Control Mode: {}".format(controlMode)
            cnt.message = message
            
            #Update arm servo positions based on changes made in event handlers
            if turnValue != 0 :
                newBase = posBase + (turnValue * turnSpeed)
                if arm.turnMin <= newBase <= arm.turnMax :
                    posBase = newBase
                    arm.setArmPosition ( arm.turnChannel, posBase )

            if jawsChange != 0 :
                newJaws = posJaws + (jawsChange * jawsSpeed)
                if arm.jawsMin <= newJaws <= arm.jawsMax :
                    posJaws = newJaws
                    arm.setArmPosition ( arm.jawsChannel, posJaws )
                    
            if controlMode == 1:
                if liftChange != 0:
                    newLift = posLift + (liftChange * liftSpeed)
                    if arm.liftMin <= newLift <= arm.liftMax:
                        posLift = newLift
                        arm.setArmPosition( arm.liftChannel, posLift )
                if reachChange != 0:
                    newReach = posReach + (reachChange * reachSpeed )
                    if arm.fwdMin <= newReach <= arm.fwdMax:
                        posReach = newReach
                        arm.setArmPosition( arm.fwdChannel, posReach )
                    

    finally:
        #Clean up and turn off Blinkt LEDs
        pygame.quit()
        if cnt.initialised :
            resetArm()

if __name__ == '__main__':
    main()
    