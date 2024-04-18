import sys
from drivers.big_easy_driver import BigEasyDriver as drive
from drivers.hc_sr04 import HCSR04Sensor as sense
from drivers.mowing_motor import MowingMotor as mow

MOWER_MOTOR_PIN = 40  # Update with the actual GPIO pin for your mower motor

# Initialize mower motor
mower_motor = mow(pwm_pin=MOWER_MOTOR_PIN)

mower_motor.set_speed(50)

while True:
    print("Enter motor speed:")
    speed = int(input())
    if 0 <= speed >= 101:
        print(speed, "is an invalid input.")
    else:
        mower_motor.set_speed(speed)
        print("Speed set to:", speed)

