from big_easy_driver import BigEasyDriver

# Define step, direction, and enable pins for your drivers
driver1 = BigEasyDriver(step_pin=11, direction_pin=12, enable_pin=13)
driver2 = BigEasyDriver(step_pin=15, direction_pin=16, enable_pin=18)

# Enable the drivers
driver1.enable()
driver2.enable()

# Move motors by steps
print("Moving motor 1 forward 200 steps")
driver1.step(200)  # Move 200 steps forward
print("Moving motor 2 backward 200 steps")
driver2.step(-200) # Move 200 steps backward

# Move motors indefinitely
print("Moving motor 1 indefinitely forward at speed 0.005")
driver1.move_indefinitely(direction='forward', speed=0.005)
print("Moving motor 2 indefinitely backward at speed 0.005")
driver2.move_indefinitely(direction='backward', speed=0.005)

# To stop indefinite movement
# driver1.stop_indefinite_move()
# driver2.stop_indefinite_move()

# Clean up GPIO resources
# driver1.cleanup()
# driver2.cleanup()
