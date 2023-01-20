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
        ilan.write("Run time: {} sec.".format(round(total_time, 1)))
        return result
    return timeit_wrapper


ilan = Robot()

##### Center Run #####


@timeit
def run_1():

    """מבצע את משימות M07,M15"""

    #  ביצוע משימה M15
    # 2023-01-18 rtm changed the run - added slide in front of arm. More accurate - so reduced 4->3 times push

    ilan.pid_gyro(14,precise_distance = False)
    ilan.turn(-45)
    ilan.speed_formula(52,500)
    
    # התיישרות על משימה M14

    ilan.turn(90)
    ilan.pid_gyro(8,Forward_Is_True = False,precise_distance = False)
    ilan.pid_gyro(16,precise_distance = False)

    #  ביצוע משימה M15
     
    for i in range (3):
        ilan.pid_gyro(12 + i,200,precise_distance = False)
        wait(500)
        ilan.pid_gyro(12,200,Forward_Is_True = False,precise_distance = False)

    # חזרה הביתה

    ilan.pid_gyro(5,400,Forward_Is_True =  False,precise_distance = False)
    ilan.turn(90,200)
    ilan.pid_gyro(58,400,precise_distance = False)



@timeit
def run_2():

    """מבצע את משימות M08,M14"""

    #  ביצוע משימה M08 

    ilan.speed_formula(41 ,400)
    ilan.speed_formula(49,400,False)

    # ביצוע משימה M14

    ilan.turn(-50,150)
    ilan.speed_formula(45,300)
    ilan.pid_gyro(2,200)

    # חזרה הביתה

    ilan.speed_formula(42,500,False)



@timeit
def run_3():
    #Worked well 14/1/23
    #ilan.pid_gyro(65,200,precise_distance = False)
    ilan.speed_formula(74, 450)
    #ilan.wait_for_button("1",True)
    #ilan.pid_follow_line_until_other_detect_color(1,ilan.color_sensor_left,ilan.color_sensor_right,80,False, kp=0.72, ki=0.02, kd=0.076)
    #ilan.pid_gyro(9,80,False)
    ilan.left_medium_motor.run_angle(400,-100)
    #ilan.wait_for_button("2",True)
    #ilan.pid_gyro(4,80)
    #ilan.turn(-2, 70)
    ilan.right_medium_motor.run_angle(350,110)
    #wait(800)
    #ilan.right_medium_motor.run_angle(300,-50)
    #wait(800)
    #ilan.right_medium_motor.run_angle(400,50)
    #ilan.turn(2, 70)

    ilan.pid_gyro(90,400,precise_distance = False)



@timeit
def run_4():

    """מבצע את משימה M04 ואוסף את יחידות המים"""

    debug = False

    # נסיעה ברוורס למשימה M04

    ilan.wait_for_button("10 - drive", debug)
    ilan.speed_formula(68,420,False,3.07)

    ilan.wait_for_button("20 - turn", debug)
    ilan.turn(-30)

    # אסיפת 2יחידות אנרגיה ממשימה M04

    ilan.wait_for_button("30 - drive", debug)
    ilan.speed_formula(25,300,False)

    # התיישרות על קו

    ilan.wait_for_button("40 - Run until color", debug)
    ilan.pid_gyro_until_color_in_one_sensor(Color.WHITE)
    ilan.wait_for_button("42 - Align on black", debug)
    ilan.straighten_on_black(60)

    # אסיפת יחידות מים

    ilan.wait_for_button("50 - drive 4.5 cm", debug)
    ilan.pid_gyro(4.5,precise_distance = False)
    ilan.beep()
    ilan.wait_for_button("60 - turn", debug)
    ilan.turn(-57)
    ilan.right_medium_motor.run_angle(1500,80,wait = False)
    ilan.pid_gyro(17,precise_distance = False)
    ilan.right_medium_motor.run_angle(-150,90)

    # נסיעה על קו

    ilan.turn(-32)
    ilan.pid_gyro_until_color_in_one_sensor()
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
    ilan.turn(-30)
    ilan.pid_gyro(22,170,precise_distance = False)

    #שפיכת יחידות האנרגיה למשימה 

    ilan.pid_gyro(7,270,precise_distance = False)

    #לקיחת יחידת האנרגיה וחזרה הביתה

    ilan.pid_gyro(30,300,False,precise_distance = False)
    ilan.turn(30)
    ilan.pid_gyro(40,300,False,precise_distance = False)



@timeit
def run_6a():

    ilan.speed_formula(85, Kp=3.1, Ki=0.03)
    ilan.pid_gyro_until_color_in_one_sensor(Ts = 100)
    ilan.pid_gyro_until_color_in_one_sensor(Color.WHITE,100)
    ilan.pid_gyro(3, 80,precise_distance = False)
    ilan.turn(-125)
    ilan.pid_gyro(12, 120,precise_distance = False)
    #ilan.drive_by_seconds(100,1.5)
    ilan.robot.drive(150, 0)
    wait(1300)
    ilan.robot.stop()

    ilan.right_medium_motor.run_angle(200, -135)
    ilan.pid_gyro(20, 150, False,precise_distance = False)
    ilan.turn(-50) 
    ilan.pid_gyro(65,300,precise_distance = False) 
#    ilan.pid_gyro(72,300,precise_distance = False)
#    ilan.turn(-105)
#    ilan.pid_gyro(17,precise_distance = False)
#    ilan.right_medium_motor.run_angle(200,-135)
#    ilan.pid_gyro(17,Forward_Is_True = False, precise_distance = False)
#    ilan.turn(115)
#    ilan.pid_gyro(73,300,False,precise_distance = False)

@timeit
def run_6b():

    ilan.pid_gyro(70,Forward_Is_True = False,precise_distance = False)
    ilan.turn(50)
    ilan.pid_gyro(12, 120,precise_distance = False)
    #ilan.drive_by_seconds(100,1.5)
    ilan.robot.drive(80, 0)
    wait(1500)
    ilan.robot.stop()

    ilan.right_medium_motor.run_angle(200, -135)
    ilan.pid_gyro(20, 150, False,precise_distance = False)
    ilan.turn(-50) 
    ilan.pid_gyro(80,300,precise_distance = False) 
#    ilan.pid_gyro(72,300,precise_distance = False)
#    ilan.turn(-105)
#    ilan.pid_gyro(17,precise_distance = False)
#    ilan.right_medium_motor.run_angle(200,-135)
#    ilan.pid_gyro(17,Forward_Is_True = False, precise_distance = False)
#    ilan.turn(115)


TEXT_MENU = """Choose Run: 
  < - Left run 
  > - Right AP 
  O - Center run 
  V - Down run 
  ^ - Up run"""



##### פונקציה להפעלת הריצות באמצעות כפתורי הרובוט #####

def running ():
    
    """!! One Function To Rule Them All !!"""

    ilan.say("Started")
    situation = "1-4"
    ilan.write("\t2\n3   v   1\n\t4")

    while True:

        if Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "1-4":
            run_1()
        elif  Button.RIGHT in ilan.ev3.buttons.pressed() and situation == "3-6":
            run_5()
        
        if Button.UP in ilan.ev3.buttons.pressed() and situation == "1-4":
            run_2()
        elif  Button.UP in ilan.ev3.buttons.pressed() and situation == "3-6":
            run_6b()

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
