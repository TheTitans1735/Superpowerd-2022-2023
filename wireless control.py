#!/usr/bin/env pybricks-micropython

import pygame
from pybricks.tools import wait

from robot import *

# pygame.init()
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
        for event in event.pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and situation == "drive":
                # ilan.wait_for_button("if drive: turn right \n if motors: motors right", if_wait)
                    """Move wall to right"""
                    print(situation)
                    ilan.left_motor.run(50)
                    ilan.right_motor.run(-50)
                elif event.key == pygame.K_RIGHT and situation == "motor":
                    ilan.left_medium_motor.dc(50)
                    ilan.right_medium_motor.dc(50)

                if event.key == pygame.K_LEFT  and situation == "drive":
                    ilan.left_motor.run(-50)
                    ilan.right_motor.run(50)

                elif event.key == pygame.K_LEFT  and situation == "motor":
                    ilan.left_medium_motor.dc(-50)
                    ilan.right_medium_motor.dc(-50)
                    

                if event.key == pygame.K_UP and situation == "drive":
                    ilan.left_motor.run(speed)
                    ilan.right_motor.run(speed)

                if event.key == pygame.K_DOWN:
                    
                    ilan.left_motor.run(-1 * speed)
                    ilan.right_motor.run(-1 * speed)

                if event.key == pygame.K_SPACE:  
                    if situation == "drive":
                        situation = "motor"
                    else:
                        situation = "drive"
