# Examples and Template

This folder contains the examples for using Pygame Controller with various hardware add-on boards (HATS), and a template project file which you can use to get started writing your own programs. There are currently examples using the following HATs:

#AdaFruit ServoHAT

[MeArmServoControl.py](/AdaFruit_ServoHAT/MeArmServoControl.py) This module contains the code for controlling the servos on a MeArm robot arm using the AdaFruit ServoHAT. As each MeArm will be assembled with the servos in slightly rotations, you will want to edit the constants in this file to set the rotation limits (minimum and maximum rotation of each servo in degrees) for your own MeArm. This module contains a test method for the servos which is run when this module is executed directly. When this module is imported into other Python programs it provides methods to set the positions of all the servos in degrees, limiting them to the min. and max. limits which you can configured to prevent any servo being set to beyond the positions it can reach when fitted in a robot arm.

[MeArm.py](/AdaFruit_ServoHAT/MeArm.py) This module uses the MeArmServoControl.py with PygameController to interface the servos on a MeArm to a game controller.

#Pimoroni Blinkt

[BlinktController.py](/Blinkt/BlinktController.py) This module demonstrates how different controls on a game controller can be interfaced to your code using PygameController and the 8 RGB LED Blinkt add-on. It includes an example of an initialise callback function which indicates when the program is waiting for a bluetooth controller to be paired, when a supported controller is successfully detected, and when no supported controller is found. This initialise method is reused in some of the robot examples where a Blinkt is attached for feedback in addition to a robot controller HAT.

#4Tronix Picon Zero robot controller pHAT

[LegoPiconZeroRobot.py](/PiconZero/LegoPiconZeroRobot.py) A simple robot controller example interfacing the left joystick to a motor and the right joystick to a servo (controlling steering).

[ZumoPiconZeroRobot.py](/PiconZero/ZumoPiconZeroRobot.py) A more complex robot example using two motors for steering, a Blinkt for feedback and an ultrasonic HCSR04 sensor to detect distance to obstacles.

[hcsr04_bcm.py](/PiconZero/hcsr04_bcm.py) Code to read the hcsr04 ultrasonic distance sensor attached to a Picon Zero board. This module uses GPIO BCM numbering mode which enables it to be used at the same time as the Blinkt add-on. It also includes a method to read multiple samples from the sensor and process the readings to return a more stable distance reading by ignoring readings which are much less or greater than the majority of the readings from the sensor (helpful when the ultrasonic pings are bouncing off multiple objects and sometimes returns the distance to a more distant object than the nearest one).
