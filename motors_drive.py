#!/usr/bin/env pybricks-micropython

from pybricks.tools import wait

from robot import *

'''
Move the wall accordingly to the buttons
'''
            
ilan = Robot()

default_speed = 150
speed = default_speed # Start with default speed

situation = "motor"
ilan.write("motor")

if_wait = True
ilan.gyro_sensor.reset_angle(0)
while True:
    while not any(ilan.ev3.buttons.pressed()):
        wait(10)

    # Respond to the Brick Button press.
    while True:
        motor_speed = 250
        situation == "motor"
        if Button.CENTER in ilan.ev3.buttons.pressed() and situation == "motor":  
            situation = "drive"
            print("situation is:" + situation)

        elif Button.CENTER in ilan.ev3.buttons.pressed() and situation == "drive":
            situation = "motor"
            print("situation is:" + situation)

        angle = str(ilan.gyro_sensor.angle())
        if Button.UP in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.right_medium_motor.run(-1 * motor_speed)

        elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.right_medium_motor.run(motor_speed)

        elif Button.DOWN in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.left_medium_motor.run(-1 * motor_speed)

        elif Button.LEFT in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.left_medium_motor.run(motor_speed)

        elif Button.UP in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.right_motor.run(motor_speed)
                ilan.right_motor.run(motor_speed)

        elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.right_motor.run(-1 * motor_speed)
                ilan.left_motor.run(motor_speed)

        elif Button.DOWN in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.left_motor.run(-1 * motor_speed)
                ilan.right_motor.run(-1 * motor_speed)

        elif Button.LEFT in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.right_motor.run(motor_speed)
                ilan.left_motor.run(-1 * motor_speed)
        else:
            ilan.left_motor.hold()
            ilan.right_motor.hold()
            ilan.left_medium_motor.hold()
            ilan.right_medium_motor.hold()




