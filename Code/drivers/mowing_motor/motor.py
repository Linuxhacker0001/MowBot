import sys
#from drivers.GPIOEmu.EmulatorGUI import GPIO
import RPi.GPIO as GPIO

# setting path
sys.path.append('../drivers')

class MowingMotor:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin

        GPIO.setmode(GPIO.BOARD)
#        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pwm_pin, 1000)  # Frequency: 1000 Hz
        self.pwm.start(0)  # Start PWM with duty cycle 0

    def set_speed(self, speed):
        # Speed should be between 0 and 100
        if 0 <= speed <= 100:
            self.pwm.ChangeDutyCycle(speed)
        else:
            raise ValueError("Speed should be between 0 and 100")

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()