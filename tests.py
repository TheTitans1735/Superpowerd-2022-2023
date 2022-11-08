#!/usr/bin/env pybricks-micropython
from robot import *

ilan = Robot()

##### Center Run #####

def test_run():

    #ilan.run_straight(30)
    #ilan.run_straight(-30)
    ilan.turn(90)
    ilan.turn(-90)
    ilan.say("succes")

def center_run():
    """ Crane | Containers on Deck | Small Truck | Parking """

    my_debug  = False
    wall_debug = False

    # הזזת הקיר לקראת ההרצה
    ilan.move_wall_to_point(ilan.WALL_MAX_ANGLE_X / 2, ilan.WALL_MAX_ANGLE_Y, x_wait = False)
    ilan.wait_for_button("Place Arm", True)

    ## משימת המנוף ##
    # נסיעה עד הקו השחור
    ilan.wait_for_button("Drive to line", my_debug)
    ilan.pid_gyro(27, 150)

    # נסיעה על הקו השחור עד זיהוי שני קוים שחורים עם החיישן השמאלי
    ilan.wait_for_button("Drive until detect 2 lines", my_debug)
    ilan.pid_follow_line_until_other_detect_color(2, ilan.color_sensor_right, ilan.color_sensor_left, 120, False)
    
    # פנייה צפונה לכיוון המשימות
    ilan.turn(-90, 180)

    # פנייה אל הקו השחור
    ilan.wait_for_button("Turn to line", False)
    ilan.turn_to_threshold(ilan.color_sensor_right, False, 25)

    # מעקב על הקו השחור + נסיעה ישרה
    ilan.wait_for_button("Follow line & gyro to mission", my_debug)
    ilan.pid_follow_line(12, 90, ilan.color_sensor_right, white_is_right = True) 
    ilan.pid_gyro(12 - 2 + 0.3, 150)

    # פנייה מזרחה אל המנוף
    ilan.wait_for_button("Turn to crane", my_debug)
    ilan.turn(90, 170)

    # הזזת הקיר לדחיפת המנוף תוך כדי פנייה אל הקו השחור
    ilan.wait_for_button("Move wall to push crane", wall_debug)
    ilan.move_wall_to_point(0, ilan.WALL_MAX_ANGLE_Y - 200, x_wait = False, y_wait = False)

    ilan.robot.stop()
    wait(100)

    # נסיעה איטית לאחור - חנייה והפלת החלק הצהוב
    ilan.pid_gyro(10, 50, False)
    
    # (: זה הג'וק שהקפיץ את השפריץ של המיץ לעציץ על השפיץ של הקפיץ בחריץ המסוכן האור ההר
    # ilan.say("ze hajuk shehekpitz et hashpritz shel hamitlahatzitz al hashpitz shel hakfitz baharitz hamesukan behor hahar")

def fast_to_slow_stop(ts1,td1,ts2,td2):
    ts =300

def left_run():
    ilan.say(" ish mi billy otten dotten")
    ilan.straighten_on_black()
def right_run():
    ilan.run_straight(200)
    ilan.turn(90,180)

def up_run():
    ilan.run_straight(10)

def down_run():
    ilan.say("start")
    ilan.move_wall_to_point(430, 370)
    ilan.pid_gyro(30, 300)
    ilan.pid_gyro_until_color(stop_color = Color.BLACK, Ts = 20, Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02)
        
    


TEXT_MENU = """Choose Run: 
  < - Left run 
  > - Right AP 
  O - Center run 
  V - Down run 
  ^ - Up run"""


##### פונקציה להפעלת הריצות באמצעות כפתורי הרובוט #####

def running ():
    """!! One Function To Rule Them All !!"""
    
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
                test_run() # הפעלת הריצה


            # כפתור ימני - ראן צפון מערב
            elif Button.RIGHT in ilan.ev3.buttons.pressed():

                ilan.write("Right Run")
                right_run() # הפעלת הריצה


            # כפתור תחתון - ראן מזרח (מכולות קרובות)
            elif Button.DOWN in ilan.ev3.buttons.pressed():

                ilan.write("Down run")
                down_run() # הפעלת הריצה (מכולות קרובות)


            # כפתור עליון - ראן מזרח (מכולות רחוקות)
            elif Button.UP in ilan.ev3.buttons.pressed():

                ilan.write("UP run")
                up_run() # הפעלת הראן (מכולות רחוקות)


            elif Button.CENTER in ilan.ev3.buttons.pressed():

                ilan.write("Center run")
                center_run() # הפעלת הראן


        except Exception as ex:
            print("Error: {}".format(ex))
            wait(2500)

#ilan.say("auri serbero. aoyb ir farshteyn mir, ir zent a nul vos rizembalz milkh in a liter kartan.", 'de')
running()

# north_west_run()
# south_run_2022_03_09()

# # הזזה מהירה של הגלגלים 
# ilan.write("Start moving wheels")
# ilan.beep()
# while True:
#         ilan.right_motor.run(500)
#         ilan.left_motor.run(500)
