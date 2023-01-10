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
def run_3():
    pass



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
   


@timeit
def run_5(): 

    """ביצוע משימה M03"""

    #נסיעה לM03

    ilan.pid_gyro(44,150,precise_distance = False)
    ilan.turn(-32)
    ilan.pid_gyro(20,200,precise_distance = False)

    #שפיכת יחידות האנרגיה למשימה

    ilan.pid_gyro(7,300,precise_distance = False)

    #לקיחת יחידת האנרגיה וחזרה הביתה

    ilan.pid_gyro(30,300,False,precise_distance = False)
    ilan.turn(30)
    ilan.pid_gyro(40,300,False,precise_distance = False)



@timeit
def run_6():

    """ביצוע משימות M11,M12"""

    ilan.speed_formula(80,600)
    ilan.turn(60)
    ilan.pid_gyro(80,200,False,precise_distance = False)
    ilan.turn(-5)
    ilan.pid_gyro(20,200,precise_distance = False)





TEXT_MENU = """Choose Run: 
  < - Left run 
  > - Right AP 
  O - Center run 
  V - Down run 
  ^ - Up run"""



##### פונקציה להפעלת הריצות באמצעות כפתורי הרובוט #####

def running ():
    
    """!! One Function To Rule Them All !!"""

    situation = "1-4"
    ilan.write("\t2\n3\  v  t1\n\t4")

    while True:

            
            
        if Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "1-4":
            run_1()
        elif  Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "3-6":
            run_5()
        
        if Button.UP in ilan.ev3.buttons.pressed() and situation == "1-4":
            run_2()
        elif  Button.UP in ilan.ev3.buttons.pressed() and situation == "3-6":
            run_6()

        if Button.LEFT in ilan.ev3.buttons.pressed():
            run_3()

        if Button.DOWN in ilan.ev3.buttons.pressed():
            run_4()

        if Button.CENTER in ilan.ev3.buttons.pressed() and situation == "1-4":
            situation = "3-6"
            ilan.write("\t6\n3\t5\n\t4")

        elif Button.CENTER in ilan.ev3.buttons.pressed() and situation == "3-6":
            situation = "1-4"
            ilan.write("\t2\n3\t1\n\t4")



    # except Exception as ex:
    # print("Error: {}".format(ex))
    # wait(2500)

running()
