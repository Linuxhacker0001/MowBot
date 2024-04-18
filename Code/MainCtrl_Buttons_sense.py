#!/usr/bin/env python
import sys
sys.path.append("/path/to/your/packages")  # Update with the actual path to your packages

from webiopi import *
from drivers.big_easy_driver import BigEasyDriver as drive
from drivers.hc_sr04 import HCSR04Sensor as sense
from drivers.mowing_motor import MowingMotor as mow

# Define sensor check frequency/interval in seconds
sensecheck_interval = 2

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

# Function to periodically check sensors and stop the mower if obstacle detected
def sensor_check():
    while True:
        for sensor in sensors:
            distance = sensor.measure_distance()
            if distance < 30:  # Adjust threshold distance as needed
                mower_motor.set_speed(0)
                print("Obstacle detected! Mower stopped.")
                break
        time.sleep(sensecheck_interval)  # Check sensors every "sensecheck_interval"

# Start sensor check thread
sensor_thread = threading.Thread(target=sensor_check)
sensor_thread.daemon = True
sensor_thread.start()

# Initialize ultrasonic sensors
SENSOR_PINS = {
    'trigger_pin': 22,
    'echo_pin': 23
}

sensor_front = sense(**SENSOR_PINS)
sensor_left = sense(trigger_pin=24, echo_pin=25)
sensor_right = sense(trigger_pin=26, echo_pin=27)

# Define macros for controlling the mower and handling obstacle detection

@webiopi.macro
def ButtonForward():
    if not obstacle_detected():
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

# Function to check if an obstacle is detected
def obstacle_detected():
    if sensor_front.measure_distance() < 10:  # Adjust distance threshold as needed
        # Display warning message on control website
        return True
    return False

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
    sensor_front.cleanup()
    sensor_left.cleanup()
    sensor_right.cleanup()
    pass
