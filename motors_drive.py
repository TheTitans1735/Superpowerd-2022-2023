#!/usr/bin/env pybricks-micropython

from pybricks.tools import wait

from robot import *

'''
Move the wall accordingly to the buttons
'''

ilan = Robot()
ilan.beep()

default_speed = 100
speed = default_speed # Start with default speed

situation = "motor"

if_wait = True

ilan.write("Use buttons to move wall")
while True:
    while not any(ilan.ev3.buttons.pressed()):
        wait(10)

    # Respond to the Brick Button press.
    while True:
        
        if Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "drive":
           # ilan.wait_for_button("if drive: turn right \n if motors: motors right", if_wait)
            """Move wall to right"""
            print(situation)
            ilan.left_motor.run(50)
            ilan.right_motor.run(-50)
        elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "motor":
            ilan.left_medium_motor.dc(50)
            ilan.right_medium_motor.dc(50)

        elif Button.LEFT in ilan.ev3.buttons.pressed()  and situation == "drive":
            ilan.left_motor.run(-50)
            ilan.right_motor.run(50)

        elif Button.LEFT in ilan.ev3.buttons.pressed()  and situation == "motor":
            ilan.left_medium_motor.dc(-50)
            ilan.right_medium_motor.dc(-50)
            

        elif Button.UP in ilan.ev3.buttons.pressed() and situation == "drive":
            ilan.left_motor.run(speed)
            ilan.right_motor.run(speed)

        elif Button.DOWN in ilan.ev3.buttons.pressed():
            
            ilan.left_motor.run(-1 * speed)
            ilan.right_motor.run(-1 * speed)

        elif Button.CENTER in ilan.ev3.buttons.pressed():  
            if situation == "drive":
                situation = "motor"
            else:
                situation = "drive"
        else:
            ilan.left_motor.brake()
            ilan.right_motor.brake()
            ilan.left_medium_motor.brake()
            ilan.right_medium_motor.brake()
