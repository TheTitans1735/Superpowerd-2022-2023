#!/usr/bin/env pybricks-micropython

from robot import Robot
from pybricks.parameters import Button, Color, Stop
from pybricks.tools import StopWatch, wait
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
    ilan.speed_formula(31.5,300)
    ilan.pid_gyro(10,200,False,precise_distance = False)
    ilan.turn(-45)
    ilan.speed_formula(47,400) 
    ilan.turn(95)
    ilan.drive_by_seconds(120,2)
    for i in range(4):
        ilan.drive_by_seconds(120,1)
        wait(500)
        ilan.pid_gyro(3.5,Forward_Is_True = False,precise_distance = False)
    ilan.pid_gyro(4,200,False,precise_distance = False)
    ilan.turn(90)
    ilan.drive_by_seconds(-300,1)
    ilan.turn(10)
    ilan.speed_formula(85,500)

@timeit
def run_2():

    """מבצע את משימות M08,M14"""

    #  ביצוע משימה M08 

    ilan.speed_formula(47 ,300,False)
    ilan.speed_formula(51,500)

    # ביצוע משימה M14
    #2023-01-21 rtm Add wait for button so we can lower the alignment tool manually
    # ilan.beep()
    # ilan.wait_for_button("Before Turn",True)
    # ilan.beep()
    # ilan.turn(-52,200)
    # ilan.speed_formula(48,400)
    # # ilan.run_seconds(0.5,100)
        
    # ilan.pid_gyro(2,100)

    # חזרה הביתה

    # ilan.speed_formula(42,500,False)



@timeit
def run_3():
    #Worked well 14/1/23
    #ilan.pid_gyro(65,200,precise_distance = False)
    ilan.speed_formula(71, 450)
    #ilan.pid_follow_line(2, 100, ilan.color_sensor_right, white_is_right=False)
    #ilan.wait_for_button("1",True)
    #ilan.pid_follow_line_until_other_detect_color(1,ilan.color_sensor_left,ilan.color_sensor_right,80,False, kp=0.72, ki=0.02, kd=0.076)
    #ilan.pid_gyro(9,80,False)
    ilan.left_medium_motor.run_angle(400,-100)
    #ilan.pid_follow_line(17,100, ilan.color_sensor_right, white_is_right=False)
    #ilan.wait_for_button("2",True)
    #ilan.pid_gyro(4,80)
    #ilan.turn(-2, 70)
    ilan.right_medium_motor.run_angle(350,80)
    #wait(800)
    #ilan.right_medium_motor.run_angle(300,-50)
    #wait(800)
    #ilan.  right_medium_motor.run_angle(400,50)
    #ilan.turn(2, 70)

    ilan.pid_gyro(90,400,precise_distance = False)



@timeit
def run_4():

    """מבצע את משימה M04 ואוסף את יחידות המים"""

    debug = False

    # נסיעה ברוורס למשימה M04

    ilan.speed_formula(68,420,False,3.07)
    ilan.turn(-28)

    # אסיפת יחידות האנרגיה הימניות

    ilan.speed_formula(25,300,False)

    #אסיפת יחידת האנרגיה השמאלית

    ilan.pid_gyro(10,200,precise_distance = False)
    ilan.turn(60) 
    ilan.speed_formula(27,400,False)

    #ביצוע משימה M05 

    ilan.pid_gyro(6,250,precise_distance = False)
    ilan.turn(40)
    ilan.pid_gyro(10,200,False,precise_distance = False)
    ilan.turn(-50,190)
    

    #התיישרות על קיר והגעה ליחידות המים

    ilan.pid_gyro(3,300,precise_distance= False)
    ilan.turn(-40)
    ilan.pid_gyro(10,200,False,precise_distance = False)
    ilan.right_medium_motor.run_time(200,750,wait = False)
    ilan.pid_gyro(10,200,precise_distance = False)
    ilan.turn(-10)
    ilan.pid_gyro(8,200,precise_distance = False)

    #אסיפת יחידות המים

    # ilan.turn(-27)
    # ilan.pid_gyro(8,200,precise_distance = False)
    ilan.right_medium_motor.run_angle(150,-110)

    # ביצוע משימה  M05 וחזרה הביתה
    ilan.turn(-20)
    ilan.pid_gyro(40,400, precise_distance=False)
    ilan.turn(110,200)
    ilan.pid_gyro(100,400, precise_distance=False)
    # ilan.pid_gyro(12,300,False,precise_distance = False)    
    # ilan.turn(60)
    # ilan.speed_formula(60,600)
    # ilan.turn(-25)
    # ilan.pid_gyro(38,500,precise_distance = False)



@timeit
def run_5(): 

    """ביצוע משימה M03"""

    #נסיעה לM03

    # ilan.pid_gyro(60,150,precise_distance = False)
    ilan.speed_formula(58)
    ilan.turn(-18)
    ilan.pid_gyro(19.5,170,precise_distance = False)
    ilan.pid_gyro(6,200,False,precise_distance = False)
    for k in range(2):
        ilan.pid_gyro(6,200,precise_distance = False)
        wait(500)
        ilan.pid_gyro(6,200,False,precise_distance = False)
    #שפיכת יחידות האנרגיה למשימה 

    # ilan.pid_gyro(8,270,precise_distance = False)
    #ilan.wait_for_button("sdd", True)
    # wait(500)
    

    #לקיחת יחידת האנרגיה וחזרה הביתה

    ilan.pid_gyro(25,300,False,precise_distance = False)
    ilan.turn(30)
    ilan.pid_gyro(55,300,False,precise_distance = False)
    
def run_5a(): 

    """ביצוע משימה M03"""

    #נסיעה לM03

    # ilan.pid_gyro(60,150,precise_distance = False)
    ilan.speed_formula(57)
    ilan.turn(-18)
    ilan.pid_gyro(19.5,170,precise_distance = False)
    ilan.pid_gyro(6,200,False,precise_distance = False)
    for k in range(2):
        ilan.pid_gyro(6,200,precise_distance = False)
        wait(500)
        ilan.pid_gyro(6,200,False,precise_distance = False)
    #שפיכת יחידות האנרגיה למשימה 

    # ilan.pid_gyro(8,270,precise_distance = False)
    #ilan.wait_for_button("sdd", True)
    # wait(500)
    

    #לקיחת יחידת האנרגיה וחזרה הביתה

    ilan.pid_gyro(25,300,False,precise_distance = False)
    ilan.turn(30)
    ilan.pid_gyro(55,300,False,precise_distance = False)
    
@timeit
def run_6():
    
    

    """ביצוע M11 ו M12"""

    # הגעה והתייצבות על הסכר

    ilan.pid_gyro(70,Forward_Is_True = False,precise_distance = False)
    ilan.turn(50)
    ilan.pid_gyro(12, 120,precise_distance = False)

    # שחרור יחידת האנרגייה ותליית יחידות המים

    ilan.robot.drive(80, 0)
    wait(1000)
    ilan.robot.drive(55, 0)
    wait(1400)
    ilan.robot.stop()

    # חזרה הביתה

    ilan.right_medium_motor.run_angle(200, -220)
    ilan.pid_gyro(20, 150, False,precise_distance = False)
    ilan.turn(-50) 
    ilan.pid_gyro(80,300,precise_distance = False) 
#    ilan.pid_gyro(72,300,precise_distance = False)
#    ilan.turn(-105)
#    ilan.pid_gyro(17,precise_distance = False)
#    ilan.right_medium_motor.run_angle(200,-135)
#    ilan.pid_gyro(17,Forward_Is_True = False, precise_distance = False)
#    ilan.turn(115)


@timeit
def run_6a():

    """הצבה קדימה"""

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

    """הצבה אחורה"""

    ilan.pid_gyro(70,Forward_Is_True = False,precise_distance = False)
    ilan.turn(50)
    ilan.pid_gyro(12, 120,precise_distance = False)
    #ilan.drive_by_seconds(100,1.5)
    ilan.robot.drive(80, 0)
    wait(1000)
    ilan.robot.drive(55, 0)
    wait(1400)
    ilan.robot.stop()

    ilan.right_medium_motor.run_angle(200, -140)
    ilan.right_medium_motor.run_angle(150, 140, wait=False)
    ilan.pid_gyro(20, 150, False,precise_distance = False)
    ilan.turn(-50) 
    ilan.pid_gyro(80,300,precise_distance = False) 
#    ilan.pid_gyro(72,300,precise_distance = False)
#    ilan.turn(-105)
#    ilan.pid_gyro(17,precise_distance = False)
#    ilan.right_medium_motor.run_angle(200,-135)
#    ilan.pid_gyro(17,Forward_Is_True = False, precise_distance = False)
#    ilan.turn(115)

def run_6c():

        #11/1 איה ורתם עדכנו לא לגעת עד לבנית סרגל שיגור
    """פנאומטי"""
    ilan.beep()
    ilan.speed_formula(65,300)
    #ilan.pid_gyro(20,200,True,precise_distance = True)
    
    ilan.turn(75)
    
    ilan.pid_gyro(11,90,False,precise_distance = True)
    ilan.wait_for_button()
    ilan.turn(-10)
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

    ilan.beep()
        # ilan.write(TEXT_MENU)
       
    Runs = [
        ("Run 1", run_1),
        ("Run 2", run_2),
        ("Run 3", run_3),
        ("Run 4", run_4),
        ("Run 5", run_5),
        ("Run 6", run_6) 
    ]

    current_run = 0
    ilan.write(Runs[current_run][0])
    elsapsed_time = StopWatch()

    while True:

        try:
        

            if (Button.UP in ilan.ev3.buttons.pressed()):
                current_run += 1

                if current_run >= len(Runs):
                    current_run = 0
                    
                ilan.write(Runs[current_run][0])

                wait(300)

            if (Button.DOWN in ilan.ev3.buttons.pressed()):
                current_run -= 1

                if current_run < 0:
                    current_run = len(Runs) - 1
            
                ilan.write(Runs[current_run][0])
                
                wait(300)

            if Button.CENTER in ilan.ev3.buttons.pressed():

                if current_run == 0:
                    elsapsed_time.reset()

                Runs[current_run][1]()
            
                current_run += 1

                if current_run >= len(Runs):
                    current_run = 0

                ilan.write("Elapsed: {} s \n{}".format(round(elsapsed_time.time()/1000.0, 1), Runs[current_run][0]))
        except Exception as EX :
            print(str(EX))
            wait(1500)
            
            
running()
