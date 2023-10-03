#!/usr/bin/env pybricks-micropython

from pybricks.tools import wait
from pybricks.parameters import Button
from robot import *

'''
Move the wall accordingly to the buttons

drive:          right
                  |
          up <---stop---> down
                  |
                left
'''
            
ilan = Robot()

default_speed = 150
speed = default_speed # Start with default speed

situation = "motor"
ilan.write("default: motor")

if_wait = True
ilan.gyro_sensor.reset_angle(0)
while True:
    while not any(ilan.ev3.buttons.pressed()):
        wait(10)

    # Respond to the Brick Button press.
    while True:
        motor_speed = 250
        situation == "motor"
        #motor
        if Button.CENTER in ilan.ev3.buttons.pressed() and situation == "motor":  
            situation = "drive"
            ilan.write("!!wait!!")
            wait(500)
            ilan.write("situation: drive\n\ncontroller:\n\t\t\tright\t\t\t\n  up\t\t\tdown\n\t\t\tleft\t\t\t\t")

        elif Button.CENTER in ilan.ev3.buttons.pressed() and situation == "drive":
            situation = "motor"
            ilan.write("!!wait!!")
            wait(500)
            ilan.write("situation: motor")
#               right
#                  |
#          up <---stop---> down
#                  |
#                left


        angle = str(ilan.gyro_sensor.angle())
        if Button.UP in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.right_medium_motor.run(-1 * motor_speed)

        elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.right_medium_motor.run(motor_speed)

        elif Button.DOWN in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.left_medium_motor.run(-1 * motor_speed)

        elif Button.LEFT in ilan.ev3.buttons.pressed() and situation == "motor":
                ilan.left_medium_motor.run(motor_speed)

        # drive
        elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.right_motor.run(motor_speed)
                ilan.left_motor.run(motor_speed)

        elif Button.DOWN in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.right_motor.run(-1 * motor_speed)
                ilan.left_motor.run(motor_speed)

        elif Button.LEFT in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.left_motor.run(-1 * motor_speed)
                ilan.right_motor.run(-1 * motor_speed)

        elif Button.UP in ilan.ev3.buttons.pressed() and situation == "drive":
                ilan.right_motor.run(motor_speed)
                ilan.left_motor.run(-1 * motor_speed)
        else:
            ilan.left_motor.hold()
            ilan.right_motor.hold()
            ilan.left_medium_motor.hold()
            ilan.right_medium_motor.hold()

