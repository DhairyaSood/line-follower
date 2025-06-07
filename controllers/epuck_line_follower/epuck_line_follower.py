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

sensor_names = ['ir0', 'ir3', 'ir4', 'ir2', 'ir1']
sensors = []
for name in sensor_names:
    sensor = robot.getDevice(name)
    sensor.enable(time_step)
    sensors.append(sensor)

def black_line(value):
    if value > 5:
        return True
    else:
        return False

while robot.step(time_step) != -1:
    sensor_values = []
    for sensor in sensors:
        sensor_values.append(sensor.getValue())

    sensor_states = []
    for val in sensor_values:
        if black_line(val):
            sensor_states.append(1)
        else:
            sensor_states.append(0)

    print("Sensor readings:", sensor_values)
    print("Line detected:", sensor_states)

    left_far = sensor_states[0]    # ir0
    left_mid = sensor_states[1]    # ir3
    center = sensor_states[2]      # ir4
    right_mid = sensor_states[3]   # ir2
    right_far = sensor_states[4]   # ir1

    if center == 1:
        left_motor.setVelocity(fast_speed)
        right_motor.setVelocity(fast_speed)
    elif left_mid == 1:
        left_motor.setVelocity(medium_speed)
        right_motor.setVelocity(fast_speed)
    elif right_mid == 1:
        left_motor.setVelocity(fast_speed)
        right_motor.setVelocity(medium_speed)
    elif left_far == 1:
        left_motor.setVelocity(slow_speed)
        right_motor.setVelocity(fast_speed)
    elif right_far == 1:
        left_motor.setVelocity(fast_speed)
        right_motor.setVelocity(slow_speed)
    else:
        left_motor.setVelocity(0)
        right_motor.setVelocity(0)
