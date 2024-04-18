import sys
#from drivers.GPIOEmu.EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import time

# setting path
sys.path.append('../drivers')

class HCSR04Sensor:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def measure_distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        start_time = time.time()
        end_time = time.time()

        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()

        while GPIO.input(self.echo_pin) == 1:
            end_time = time.time()

        duration = end_time - start_time
        distance = duration * 17150  # Speed of sound is approximately 343 m/s

        return distance

    def cleanup(self):
        GPIO.cleanup()
