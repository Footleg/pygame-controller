# Examples and Template

This folder contains the examples for using Pygame Controller with various hardware add-on boards (HATS), and a template project file which you can use to get started writing your own programs. There are currently examples using the following HATs:

## AdaFruit ServoHAT

[MeArmServoControl.py](/examples/AdaFruit_ServoHAT/MeArmServoControl.py) This module contains the code for controlling the servos on a MeArm robot arm using the AdaFruit ServoHAT. When fitted to a MeArm, the servos cannot rotate through their full 180 degree range because the different parts of the arm do not allow this much movement. Each MeArm will be assembled with the servos in slightly different rotations, you will want to edit the constants in this file to set the rotation limits (minimum and maximum rotation of each servo in degrees) for your own MeArm. This module contains a test method for the servos which is run when this module is executed directly. When this module is imported into other Python programs it provides methods to set the positions of all the servos in degrees, limiting them to the min. and max. limits which you can configured to prevent any servo being set to beyond the positions it can reach when fitted in a robot arm.

[MeArm.py](/examples/AdaFruit_ServoHAT/MeArm.py) This module uses the MeArmServoControl.py with PygameController to interface the servos on a MeArm to a game controller.

## Pimoroni Blinkt

[BlinktController.py](/examples/Blinkt/BlinktController.py) This module demonstrates how different controls on a game controller can be interfaced to your code using PygameController and the 8 RGB LED Blinkt add-on. It includes an example of an initialise callback function which indicates when the program is waiting for a bluetooth controller to be paired, when a supported controller is successfully detected, and when no supported controller is found. This initialise method is reused in some of the robot examples where a Blinkt is attached for feedback in addition to a robot controller HAT. This module also includes a method to display the IP address of a Raspberry Pi on the Blinkt, for when no monitor is connected and you want to VNC onto to Pi.

## 4tronix Picon Zero robot controller pHAT

[LegoPiconZeroRobot.py](/examples/PiconZero/LegoPiconZeroRobot.py) A simple robot controller example interfacing the left joystick up/down position to control the speed and direction of a motor (driving the back wheels) and the right joystick to a servo (controlling steering of the front wheels). My robot was built using a standard servo and a Lego Power Functions motor, but this example will suit any robot using a single motor for drive, and a servo for steering.

[ZumoPiconZeroRobot.py](/examples/PiconZero/ZumoPiconZeroRobot.py) A more complex robot example using two motors for steering, a Blinkt for feedback and an ultrasonic HCSR04 sensor to detect distance to obstacles. My robot was built using a Pololu Zumo chassis but it will suit any robot using separate motors for left and right wheels of tracks for drive and steering. The distance readings are just displayed on the program UI currently, to demonstrate how to display additional information in the application window and how to get readings from the sensor. 

[hcsr04_bcm.py](/examples/PiconZero/hcsr04_bcm.py) Code to read the hcsr04 ultrasonic distance sensor attached to a Picon Zero board. This module uses GPIO BCM numbering mode which enables it to be used at the same time as the Blinkt add-on. It also includes a method to read multiple samples from the sensor and process the readings to return a more stable distance reading by ignoring readings which are much less or greater than the majority of the readings from the sensor (helpful when the ultrasonic pings are bouncing off multiple objects and sometimes return the distance to a more distant object instead of the nearest one).
