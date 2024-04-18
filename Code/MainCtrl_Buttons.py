#!/usr/bin/env python
import sys
import webiopi
from big_easy_driver import BigEasyDriver as drive
from hc_sr04 import HCSR04Sensor as sense
from mowing_motor import MowingMotor as mow

#sys.path.append("/home/admin/robot/Code/drivers")  # Update with the actual path to your packages


# Define GPIO pins for the motor drivers
LEFT_DRIVER_PINS = {
    'step_pin': 11,
    'direction_pin': 12,
    'enable_pin': 13
}

RIGHT_DRIVER_PINS = {
    'step_pin': 15,
    'direction_pin': 16,
    'enable_pin': 18
}

MOWER_MOTOR_PIN = 21  # Update with the actual GPIO pin for your mower motor

# Initialize motor drivers
left_driver = drive(**LEFT_DRIVER_PINS)
right_driver = drive(**RIGHT_DRIVER_PINS)

# Initialize mower motor
mower_motor = mow(pwm_pin=MOWER_MOTOR_PIN)

# Set initial speed for motor drivers
left_driver.set_speed(0)
right_driver.set_speed(0)

# Set initial speed for mower motor
mower_motor.set_speed(0)

# Define macros for controlling the mower

@webiopi.macro
def ButtonForward():
    left_driver.move_indefinitely(direction='forward', speed=0.5)
    right_driver.move_indefinitely(direction='forward', speed=0.5)

@webiopi.macro
def ButtonReverse():
    left_driver.move_indefinitely(direction='backward', speed=0.5)
    right_driver.move_indefinitely(direction='backward', speed=0.5)

@webiopi.macro
def ButtonTurnLeft():
    left_driver.move_indefinitely(direction='backward', speed=0.5)
    right_driver.move_indefinitely(direction='forward', speed=0.5)

@webiopi.macro
def ButtonTurnRight():
    left_driver.move_indefinitely(direction='forward', speed=0.5)
    right_driver.move_indefinitely(direction='backward', speed=0.5)

@webiopi.macro
def ButtonStop():
    left_driver.stop_indefinite_move()
    right_driver.stop_indefinite_move()

@webiopi.macro
def ButtonMowerStart():
    mower_motor.set_speed(100)  # Set mower motor speed to 100%

@webiopi.macro
def ButtonMowerStop():
    mower_motor.set_speed(0)  # Stop mower motor

# Start the WebIOPi server
def setup():
    server = Server(port=8000, login="USERNAME", password="PASSWORD")  # Replace with your desired username and password
    server.addMacro(ButtonForward)
    server.addMacro(ButtonReverse)
    server.addMacro(ButtonTurnLeft)
    server.addMacro(ButtonTurnRight)
    server.addMacro(ButtonStop)
    server.addMacro(ButtonMowerStart)
    server.addMacro(ButtonMowerStop)

# Clean up GPIO resources when the server is stopped
def destroy():
    left_driver.cleanup()
    right_driver.cleanup()
    mower_motor.cleanup()
    pass


setup()

# WebIOPi wird in einer Endlos-Schleife gestartet damit die 
# Befehle jederzeit entgegengenommen werden koennen.
webiopi.runLoop()
server.stop()
   
# Ende des Programms
