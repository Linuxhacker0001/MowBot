#!/usr/bin/env python
import sys
from webiopi import *
from drivers.big_easy_driver import BigEasyDriver as drive
from drivers.hc_sr04 import HCSR04Sensor as sense
from drivers.mowing_motor import MowingMotor as mow

sys.path.append("/path/to/your/packages")  # Update with the actual path to your packages

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

# Define GPIO pins for ultrasonic sensors
SENSOR_PINS = [
    {'trigger_pin': 22, 'echo_pin': 23},
    {'trigger_pin': 24, 'echo_pin': 25},
    {'trigger_pin': 26, 'echo_pin': 27}
]

# Initialize motor drivers
left_driver = drive(**LEFT_DRIVER_PINS)
right_driver = drive(**RIGHT_DRIVER_PINS)

# Initialize mower motor
mower_motor = mow(pwm_pin=MOWER_MOTOR_PIN)

# Initialize ultrasonic sensors
sensors = [sense(**pin) for pin in SENSOR_PINS]

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


# Define macros for controlling the mower

@webiopi.macro
def JoystickMove(x, y):
    # Convert joystick coordinates to motor speeds
    speed_left = y * 50
    speed_right = y * 50

    if x < -50:
        # Turn left
        speed_left -= abs(x) * 0.5
    elif x > 50:
        # Turn right
        speed_right -= x * 0.5

    # Limit speed values between -100 and 100
    speed_left = max(min(speed_left, 100), -100)
    speed_right = max(min(speed_right, 100), -100)

    # Set motor speeds
    left_driver.set_speed(speed_left)
    right_driver.set_speed(speed_right)

@webiopi.macro
def JoystickStop():
    left_driver.set_speed(0)
    right_driver.set_speed(0)

@webiopi.macro
def ButtonMowerStart():
    mower_motor.set_speed(100)  # Set mower motor speed to 100%

@webiopi.macro
def ButtonMowerStop():
    mower_motor.set_speed(0)  # Stop mower motor

# Define macro to stop mower when obstacle is detected
@webiopi.macro
def StopOnObstacle():
    for sensor in sensors:
        distance = sensor.measure_distance()
        if distance < 30:  # Adjust threshold distance as needed
            mower_motor.set_speed(0)
            return "Obstacle detected! Mower stopped."

# Start the WebIOPi server
def setup():
    server = Server(port=8000, login="USERNAME", password="PASSWORD")  # Replace with your desired username and password
    server.addMacro(JoystickMove)
    server.addMacro(JoystickStop)
    server.addMacro(ButtonMowerStart)
    server.addMacro(ButtonMowerStop)
    server.addMacro(StopOnObstacle)

# Clean up GPIO resources when the server is stopped
def destroy():
    left_driver.cleanup()
    right_driver.cleanup()
    mower_motor.cleanup()
    for sensor in sensors:
        sensor.cleanup()
    pass
