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
        
        angle = str(ilan.gyro_sensor.angle())
        if Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "drive":
            while Button.RIGHT in ilan.ev3.buttons.pressed():
                ilan.left_motor.run(150)
                ilan.right_motor.run(-150)
                ilan.wait_for_button(angle,debug = False)
        elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "motor":
            ilan.left_medium_motor.run(500)
            ilan.right_medium_motor.run(500)

        elif Button.LEFT in ilan.ev3.buttons.pressed()  and situation == "drive":
            while Button.LEFT in ilan.ev3.buttons.pressed():
                ilan.left_motor.run(-150)
                ilan.right_motor.run(150)
                ilan.wait_for_button(angle, debug = False)
        elif Button.LEFT in ilan.ev3.buttons.pressed()  and situation == "motor":
            ilan.left_medium_motor.run(-500)
            ilan.right_medium_motor.run(-500) 

        elif Button.UP in ilan.ev3.buttons.pressed():
            ilan.left_motor.run(speed)
            ilan.right_motor.run(speed)

        elif Button.DOWN in ilan.ev3.buttons.pressed():
            
            ilan.left_motor.run(-1 * speed)
            ilan.right_motor.run(-1 * speed)

        elif Button.CENTER in ilan.ev3.buttons.pressed():  
            if situation == "drive":
                ilan.write("motor")
                situation = "motor"
            else:
                ilan.write("drive")
                situation = "drive"
        else:
            ilan.left_motor.hold()
            ilan.right_motor.hold()
            ilan.left_medium_motor.hold()
            ilan.right_medium_motor.hold()
