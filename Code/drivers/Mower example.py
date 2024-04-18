from mowing_motor import MowingMotor

# Define PWM pin for your motor driver
motor = MowingMotor(pwm_pin=11)

# Set motor speed (between 0 and 100)
motor.set_speed(50)  # Set speed to 50%

# Clean up GPIO resources
motor.cleanup()
