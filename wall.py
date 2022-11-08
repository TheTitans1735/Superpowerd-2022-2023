#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait
from robot import *

"""
Move the wall accordingly to the buttons
"""

ilan = Robot()
ilan.beep()

# Reset the wall & values
ilan.reset_wall()

print("---")    

default_speed = 100
speed = default_speed # Start with default speed

ilan.write("Use buttons to move wall")
while True:
    # current angle
    ilan.write(str(ilan.wall_x_motor.angle()) + "," + str(ilan.wall_y_motor.angle()))
    
    # Wait until any Brick Button is pressed.
    while not any(ilan.ev3.buttons.pressed()):
        wait(10)

    # Respond to the Brick Button press.
    while True:
        
        if Button.RIGHT in ilan.ev3.buttons.pressed():
            """Move wall to right"""
            
            # Move the motor
            ilan.wall_x_motor.dc(speed)
            ilan.write(str(ilan.wall_x_motor.angle()) + ", " + str(ilan.wall_y_motor.angle()))


        if Button.LEFT in ilan.ev3.buttons.pressed():
            """Move wall to left"""

            ilan.wall_x_motor.dc(-speed)
            ilan.write(str(ilan.wall_x_motor.angle()) + ", " + str(ilan.wall_y_motor.angle()))
           

        if Button.UP in ilan.ev3.buttons.pressed():
            """Move wall up"""

            ilan.wall_y_motor.dc(speed)
            ilan.write(str(ilan.wall_x_motor.angle()) + ", " + str(ilan.wall_y_motor.angle()))


        if Button.DOWN in ilan.ev3.buttons.pressed():
            """Move wall down"""

            ilan.wall_y_motor.dc(-speed)
            ilan.write(str(ilan.wall_x_motor.angle()) + ", " + str(ilan.wall_y_motor.angle()))


        if Button.CENTER in ilan.ev3.buttons.pressed():
            """Lower wall's speed"""

            speed = speed - 10

            # If speed gets to 0, go to default speed
            if speed <= 0:
                speed = default_speed
            
            ilan.write("speed = " + str(speed))

        ilan.wall_y_motor.hold()
        ilan.wall_x_motor.hold()
    