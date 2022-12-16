#!/usr/bin/env pybricks-micropython
from robot import *

ilan = Robot()

##### Center Run #####



def run_1():
    ilan.pid_gyro(10,precise_distance = False)
    ilan.turn(-45)
    ilan.speed_formula(52,400)
    ilan.turn(90)
    ilan.pid_gyro(10,Forward_Is_True = False)
    ilan.pid_gyro(20)
    wait(1000)    
    for i in range (4):
        ilan.pid_gyro(7,precise_distance = False)
        wait(500)
        ilan.pid_gyro(7.,Forward_Is_True = False)
    ilan.turn(90)
    ilan.speed_formula(40,400)

def run_2():
    ilan.speed_formula(40.5,400)
    ilan.speed_formula(50.5,600,False)
    ilan.turn(-48)
    ilan.speed_formula(45,500)
    ilan.pid_gyro(5,200)
    ilan.speed_formula(45,600,False)
    
def run_4():
    
    ilan.speed_formula(68,420,False,3.07)
    ilan.turn(-30)
    ilan.speed_formula(25,300,False)
    ilan.straighten_on_black()
    ilan.pid_gyro(4.5)
    ilan.beep()
    ilan.turn(-57)
    ilan.right_medium_motor.run_angle(200,80)
    ilan.pid_gyro(17)
    ilan.right_medium_motor.run_angle(-200,90)
    ilan.beep()   
    ilan.turn(-32)
    ilan.pid_follow_line_until_other_detect_color(2,ilan.color_sensor_left,ilan.color_sensor_right,125,False)
    ilan.turn(65)
    ilan.speed_formula(30,300,False)
    ilan.turn(30)
    ilan.pid_gyro(2)
    ilan.turn(40)
    ilan.speed_formula(60,600)
    ilan.turn(45)
    ilan.speed_formula(40,400)
    
    
    






TEXT_MENU = """Choose Run: 
  < - Left run 
  > - Right AP 
  O - Center run 
  V - Down run 
  ^ - Up run"""


##### פונקציה להפעלת הריצות באמצעות כפתורי הרובוט #####

def running ():
    """!! One Function To Rule Them All !!"""
    
    ilan.say("please select run","m2",1000)
    while True:


        
        try:
            # מדפיס את טקסט הריצות על הרובוט ועל מסך המחשב
            
            ilan.write(TEXT_MENU)
            
            
            # מחכה ללחיצת כפתור
            while not any(ilan.ev3.buttons.pressed()):
                wait(60)
            

            # כפתור שמאלי - ראן דרום
            if Button.LEFT in ilan.ev3.buttons.pressed():
                
                ilan.write("Left Run")
                run_1() # הפעלת הריצה


            # כפתור ימני - ראן צפון מערב
            elif Button.RIGHT in ilan.ev3.buttons.pressed():

                ilan.write("Right Run")
                run_4() # הפעלת הריצה


            # כפתור תחתון - ראן מזרח (מכולות קרובות)
            elif Button.DOWN in ilan.ev3.buttons.pressed():

                ilan.write("Down run")
                pass # הפעלת הריצה (מכולות קרובות)


            # כפתור עליון - ראן מזרח (מכולות רחוקות)
            elif Button.UP in ilan.ev3.buttons.pressed():

                ilan.write("UP run")
                run_2() # הפעלת הראן (מכולות רחוקות)


            elif Button.CENTER in ilan.ev3.buttons.pressed():

                ilan.write("Center run")
                pass # הפעלת הראן


        except Exception as ex:
            print("Error: {}".format(ex))
            wait(2500)

#ilan.say("auri serbero. aoyb ir farshteyn mir, ir zent a nul vos rizembalz milkh in a liter kartan.", 'de')

running()
###############
#running()    #
              # 
###############


# north_west_run()
# south_run_2022_03_09()

# ilan.left_medium_motor.run
# # הזזה מהירה של הגלגלים 
# ilan.write("Start moving wheels")
# ilan.beep()
# while True:
#         ilan.right_motor.run(500)
#         ilan.left_motor.run(500)
# while True:
#     while not any(ilan.ev3.buttons.pressed()):
#         wait(10)

#     # Respond to the Brick Button press.
#     while True:
        
#         angle = str(ilan.gyro_sensor.angle())
#         if Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "drive":
#             ilan.left_motor.run(150)
#             ilan.right_motor.run(-150)
#             ilan.wait_for_button(angle,debug = False)
#         elif Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "motor":
#         #     ilan.left_medium_motor.run(500)
#         #     ilan.right_medium_motor.run(500)


#         elif Button.LEFT in ilan.ev3.buttons.pressed()  and situation == "drive":
#         #     ilan.left_motor.run(-150)
#         #     ilan.right_motor.run(150)
#         #     ilan.wait_for_button(angle, debug = False)
#         elif Button.LEFT in ilan.ev3.buttons.pressed()  and situation == "motor":
#         #     ilan.left_medium_motor.run(-500)
#         #     ilan.right_medium_motor.run(-500) 

#         elif Button.UP in ilan.ev3.buttons.pressed() and situation == "drive":
#         #     ilan.left_motor.run(speed)
#         #     ilan.right_motor.run(speed)

#         elif Button.DOWN in ilan.ev3.buttons.pressed():
            
#         #     ilan.left_motor.run(-1 * speed)
#         #     ilan.right_motor.run(-1 * speed)

#         elif Button.CENTER in ilan.ev3.buttons.pressed():  
#         #     if situation == "drive":
#         #         ilan.write("motor")
#         #         situation = "motor"
#         #     else:
#         #         ilan.write("drive")
#         #         situation = "drive"
#         # else:
#         #     ilan.left_motor.hold()
#         #     ilan.right_motor.hold()
#         #     ilan.left_medium_motor.hold()
#         #     ilan.right_medium_motor.hold()
