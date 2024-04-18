from hc_sr04 import HCSR04Sensor

# Define trigger and echo pins for your sensors
sensor1 = HCSR04Sensor(trigger_pin=11, echo_pin=12)
sensor2 = HCSR04Sensor(trigger_pin=13, echo_pin=15)
sensor3 = HCSR04Sensor(trigger_pin=16, echo_pin=18)

# Measure distances
distance1 = sensor1.measure_distance()
distance2 = sensor2.measure_distance()
distance3 = sensor3.measure_distance()

print("Distance from sensor 1:", distance1, "cm")
print("Distance from sensor 2:", distance2, "cm")
print("Distance from sensor 3:", distance3, "cm")

# Clean up GPIO resources
sensor1.cleanup()
sensor2.cleanup()
sensor3.cleanup()