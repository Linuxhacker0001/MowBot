import sys
#from drivers.GPIOEmu.EmulatorGUI import GPIO
import RPi.GPIO as GPIO
import time

# setting path
sys.path.append('../drivers')

class BigEasyDriver:
    def __init__(self, step_pin, direction_pin, enable_pin):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.enable_pin = enable_pin

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)

    def enable(self):
        GPIO.output(self.enable_pin, GPIO.LOW)

    def disable(self):
        GPIO.output(self.enable_pin, GPIO.HIGH)

    def step(self, steps, delay=0.005):
        GPIO.output(self.direction_pin, GPIO.HIGH if steps > 0 else GPIO.LOW)
        steps = abs(steps)
        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

    def move_indefinitely(self, direction, speed):
        GPIO.output(self.direction_pin, GPIO.HIGH if direction == 'forward' else GPIO.LOW)
        while True:
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(speed)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(speed)

    def stop_indefinite_move(self):
        GPIO.output(self.step_pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

