#!/usr/bin/env python3
""" Example of a robot using tank steering with two motors for left and right tracks.
    This robot uses the Sentinel board from Footleg Robotics. The speed and steering are
    controlled from the left and right sticks respectively, so in this example the
    change handler functions store the stick postions in variables and these are
    used to update the motor powers in the main program loop. (See the PiconZero
    Simple Twin Motor example for an alternative way to control a robot with just a
    single stick for both power and steering).
"""
import pygame #random, math
from time import sleep
from pygamecontroller import RobotController
import sentinelboard
import blinkt

#Initialise global variables
power = 0
turn = 0
minMovingSpeed = 30
message = ""
# Sets amount right stick position is divided by to make turns less twitchy
defaultStickTurnDampening = 1.5
stickTurnDampening = defaultStickTurnDampening

#Multiplier applied to speed so top speed is set when stick is not quite at maximum position
speedFactor = 1.0

sb = sentinelboard.SentinelBoard()

sb.voltage_multiplier = 0.606
print(f"Motor supply voltage: {sb.motor_voltage:.2f}")

def showBatteryStatus(v=0):
    # Display charge level
    BATT_MIN = 6.5
    BATT_MAX = 8.0
    battery_voltage = v
    if v == 0 :
        battery_voltage = sb.motor_voltage
    batt_percent = 100 * (battery_voltage - BATT_MIN) / (BATT_MAX - BATT_MIN)
    if batt_percent > 100:
        batt_percent = 100
    elif batt_percent < 0:
        batt_percent = 0
    r = int(120 - 1.2 * batt_percent)
    g = int(batt_percent)
    blinkt.set_all(r, g, 0) # Set all LEDs to show charge via colour
    blinkt.show()
    print(f"Motor supply voltage: {battery_voltage:.2f}")

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
    sb.setMotorsPower(lm,rm)


def initStatus(status):
    """Callback function which displays status during initialisation"""
    if status == 0 :
        print("Supported controller connected")
        blinkt.set_all(0,0,255)
    elif status < 0 :
        print("No supported controller detected")
        for i in range(1,7):
            blinkt.set_all(255,0,0)
            blinkt.show()
            sleep(0.25)
            blinkt.clear()
            blinkt.show()
            sleep(0.25)
    else :
        print("Waiting for controller {}".format(status) )
        if status < 9 :
            blinkt.set_pixel(status-1,96,0,96)
        elif status < 17 :
            blinkt.set_pixel(status-9,96,96,0)
        elif status < 25 :
            blinkt.set_pixel(status-17,192,40,0)
        elif status < 33 :
            blinkt.set_pixel(status-25,164,2,2)

    blinkt.show()


def leftTrigChangeHandler(val):
    """Handler function for left analogue trigger"""
    #Spin left at full speed
    global power, turn
    power = 0
    turn = -(val+1)/2


def rightTrigChangeHandler(val):
    """Handler function for right analogue trigger"""
    #Spin right at full speed
    global power, turn
    power = 0
    turn = (val+1)/2


def leftStickChangeHandler(valLR, valUD):
    """Handler function for left analogue stick"""
    global power
    power = valUD/stickTurnDampening


def rightStickChangeHandler(valLR, valUD):
    """Handler function for right analogue stick"""
    global turn
    turn = valLR/stickTurnDampening


def leftFrontBtn1Handler(val):
    global stickTurnDampening
    if val == 1 :
        stickTurnDampening = 2 # Slow mode
    else :
        stickTurnDampening = defaultStickTurnDampening


def rightFrontBtn1Handler(val):
    global stickTurnDampening
    if val == 1 :
        stickTurnDampening = 1 # Fast mode
    else :
        stickTurnDampening = defaultStickTurnDampening


def main():
    global message
    ## Check that required hardware is connected ##

    #Initialise the controller board


    #Run in try..finally structure so that program exits gracefully on hitting any
    #errors in the callback functions
    try:
        cnt = RobotController("Turbo 4WD Robot", initStatus,
                              leftTriggerChanged = leftTrigChangeHandler,
                              rightTriggerChanged = rightTrigChangeHandler,
                              leftStickChanged = leftStickChangeHandler,
                              rightStickChanged = rightStickChangeHandler,
                              leftBtn1Changed = leftFrontBtn1Handler,
                              rightBtn1Changed = rightFrontBtn1Handler)

        if cnt.initialised :
            keepRunning = True
            #Indicate success here, we are ready to run
            blinkt.set_all(0,255,0)
            blinkt.show()
            sleep(1)
            showBatteryStatus()
        else :
            keepRunning = False

        # -------- Main Program Loop -----------
        battReadInterval = 0
        battReadCounter = 0
        battV = 0
        while keepRunning == True :
            cnt.message = message


            # Trigger stick events and check for quit
            keepRunning = cnt.controllerStatus()

            message = "Power={0:.2f}, Turn={1:.2f}".format(power,turn)
            motorSpeed(power, turn)

            # Read battery voltage no more often than 20 cycles and only when motors are off
            battReadInterval = battReadInterval + 1
            if (battReadInterval > 20) and (power == 0) and (turn == 0):
                # Add battery voltage to variable to average after 10 readings
                battV = battV + sb.motor_voltage
                battReadInterval = 0 # Reset so another read will happen in 20 cycles
                battReadCounter = battReadCounter + 1
                # Update voltage indicator with average voltage reading every 10 reads
                if battReadCounter > 10:
                    showBatteryStatus(battV/battReadCounter)
                    battV = 0
                    battReadCounter = 0

    finally:
        #Clean up and turn off Blinkt LEDs
        sb.allOff()
        pygame.quit()


if __name__ == '__main__':
    main()