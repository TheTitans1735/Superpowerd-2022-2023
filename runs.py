#!/usr/bin/env pybricks-micropython
from robot import *
import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print('Function {}{} {} Took {} seconds'.format(func.__name__, args, kwargs, total_time))
        print()("run Took {} seconds".format(total_time))
        return result
    return timeit_wrapper


ilan = Robot()

##### Center Run #####


@timeit
def run_1():

    """מבצע את משימות M07,M15"""

    #  ביצוע משימה M15

    ilan.pid_gyro(10,precise_distance = False)
    ilan.turn(-45)
    ilan.speed_formula(52,500)
    
    # התיישרות על משימה M14

    ilan.turn(90)
    ilan.pid_gyro(8,Forward_Is_True = False,precise_distance = False)
    ilan.pid_gyro(20,precise_distance = False)

    #  ביצוע משימה M15
     
    for i in range (4):
        ilan.pid_gyro(12 + i,200,precise_distance = False)
        wait(500)
        ilan.pid_gyro(12,200,Forward_Is_True = False,precise_distance = False)

    # חזרה הביתה

    ilan.pid_gyro(5,200,Forward_Is_True =  False,precise_distance = False)
    ilan.turn(90)
    ilan.pid_gyro(60,400,precise_distance = False)

@timeit
def run_2():

    """מבצע את משימות M08,M14"""

    #  ביצוע משימה M08

    ilan.speed_formula(40.5,400)
    ilan.speed_formula(50.5,600,False)

    # ביצוע משימה M14

    ilan.turn(-47.5,175)
    ilan.speed_formula(45,500)
    ilan.pid_gyro(5,200)

    # חזרה הביתה

    ilan.pid_gyro(45,400,False,precise_distance = False)

@timeit
def run_4():

    """מבצע את משימה M04 ואוסף את יחידות המים"""

    debug = False

    # נסיעה ברוורס למשימה M04

    ilan.speed_formula(68,420,False,3.07)
    ilan.turn(-30)

    # אסיפת 2יחידות אנרגיה ממשימה M04

    ilan.speed_formula(25,300,False)

    # התיישרות על קו
    ilan.wait_for_button("40 - Align on black", debug)
    ilan.straighten_on_black(60)

    # אסיפת יחידות מים
    ilan.wait_for_button("50 - drive 4.5 cm", debug)
    ilan.pid_gyro(4.5,precise_distance = False)
    ilan.beep()
    ilan.wait_for_button("60 - turn", debug)
    ilan.turn(-57)
    ilan.right_medium_motor.run_angle(200,80,wait = False)
    ilan.pid_gyro(17)
    ilan.right_medium_motor.run_angle(-300,90)

    # נסיעה על קו

    ilan.turn(-32)
    ilan.pid_follow_line_until_other_detect_color(1,ilan.color_sensor_left,ilan.color_sensor_right,125,False,stop_color = Color.BLACK)

    # אסיפת יחידת האנרגיה האחרונה ממשימה M04

    ilan.turn(65)
    ilan.speed_formula(30,300,False)

    # חזרה הביתה

    ilan.turn(30)
    ilan.pid_gyro(2,precise_distance = False)
    ilan.turn(30)
    ilan.pid_gyro(105,600,precise_distance = False)
    # ilan.turn(-45)
    # ilan.pid_gyro(5,precise_distance = False)
    # ilan.turn(45)
    # ilan.speed_formula(40,400)



@timeit
def run_5():   
    ilan.pid_gyro(47,150,precise_distance = False)
    # ilan.pid_gyro_until_color_in_one_sensor(Ts = 300) 
    ilan.turn(-30)
    ilan.pid_gyro(20,200,precise_distance = False)
    ilan.pid_gyro(7,300,precise_distance = False)
    ilan.pid_gyro(75,300,False,precise_distance = False)


@timeit
def run_6():

    # הקוד המקורי
    ilan.pid_gyro(20,100,precise_distance = False,Forward_Is_True = False)
    ilan.wait_for_button("or is dum ")
    ilan.turn(-2)
    ilan.pid_gyro(10,precise_distance = False)
    ilan.pid_gyro(80,300,False,precise_distance = False)

#ניסוי התיישרות על קו
    ilan.pid_gyro_until_color1()
    ilan.straighten_on_black(100)


    ilan.speed_formula(70,300) 
    ilan.straighten_on_black(200)
    ilan.turn(55)
    ilan.speed_formula(20,300,False)
    ilan.turn(-31)
    ilan.pid_gyro(5,precise_distance = False)







TEXT_MENU = """Choose Run: 
  < - Left run 
  > - Right AP 
  O - Center run 
  V - Down run 
  ^ - Up run"""



##### פונקציה להפעלת הריצות באמצעות כפתורי הרובוט #####

def running ():
    """!! One Function To Rule Them All !!"""

    # ilan.gyro_reset()

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
                run_5() # הפעלת הריצה (מכולות קרובות)


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

running()
