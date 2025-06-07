from controller import Robot

robot = Robot()
time_step = 32

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

fast_speed = 3.0
medium_speed = 1.5
slow_speed = 0.5

# ir1 (far right) to ir9 (far left)
sensor_names = ['ir9', 'ir8', 'ir7', 'ir6', 'ir5', 'ir4', 'ir3', 'ir2', 'ir1']
sensors = [robot.getDevice(name) for name in sensor_names]
for sensor in sensors:
    sensor.enable(time_step)

def black_line(value):
    return value > 5

while robot.step(time_step) != -1:
    sensor_values = [sensor.getValue() for sensor in sensors]
    sensor_states = [1 if black_line(val) else 0 for val in sensor_values]

    print("Sensor readings:", [round(v, 2) for v in sensor_values])
    print("Line detected:", sensor_states)

    # sensor_states[0] is ir9 (leftmost), sensor_states[8] is ir1 (rightmost)
    left_far = sensor_states[0]
    left_mid_far = sensor_states[1]
    left_mid = sensor_states[2]
    center_left = sensor_states[3]
    center = sensor_states[4]
    center_right = sensor_states[5]
    right_mid = sensor_states[6]
    right_mid_far = sensor_states[7]
    right_far = sensor_states[8]

    # Priority-based movement
    if center:
        left_motor.setVelocity(fast_speed)
        right_motor.setVelocity(fast_speed)
    elif center_left or left_mid:
        left_motor.setVelocity(medium_speed)
        right_motor.setVelocity(fast_speed)
    elif center_right or right_mid:
        left_motor.setVelocity(fast_speed)
        right_motor.setVelocity(medium_speed)
    elif left_mid_far or left_far:
        left_motor.setVelocity(slow_speed)
        right_motor.setVelocity(fast_speed)
    elif right_mid_far or right_far:
        left_motor.setVelocity(fast_speed)
        right_motor.setVelocity(slow_speed)
    else:
        # Stop if no line is detected
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
