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
        return total_time
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
    ilan.turn_until_seconds(2,10)
    ilan.speed_formula(15,500)
    ilan.turn(10)
    ilan.speed_formula(65,500)


@timeit
def run_2():

    """מבצע את משימות M08,M14"""

    #  ביצוע משימה M08 

    ilan.drive_by_seconds(-300,1.5)
    ilan.drive_by_seconds(350,1.5)

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
    ilan.pid_gyro(71,200,precise_distance = False)
    # ilan.run_straight(72)
    # ilan.speed_formula(72, 450,True,3.3)
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

    ilan.speed_formula(67,420,False,3.07)
    ilan.turn(-28)

    # אסיפת יחידות האנרגיה הימניות
    ilan.speed_formula(25,300,False)


    #אסיפת יחידת האנרגיה השמאלית

    ilan.pid_gyro(10,200,precise_distance = False)
    ilan.turn(57) 
    ilan.speed_formula(27,400,False)

    #ביצוע משימה M05 

    ilan.pid_gyro(6,250,precise_distance = False)
    ilan.turn(40)
    ilan.pid_gyro(11.5,200,False,precise_distance = False)
    ilan.turn(-50,190)
    

    #התיישרות על קיר והגעה ליחידות המים

    ilan.pid_gyro(3,300,precise_distance= False)
    ilan.turn(-40,50)

    ilan.pid_gyro(13,200,False,precise_distance = False)

    ilan.right_medium_motor.run_time(200,750,wait = False)
    ilan.pid_gyro(10,200,precise_distance = False)
    ilan.pid_gyro(8,200,precise_distance = False)

    #אסיפת יחידות המים

    # ilan.turn(-27)
    # ilan.pid_gyro(8,200,precise_distance = False)
    ilan.right_medium_motor.run_angle(150,-110)
    ilan.turn(-10)

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

    ilan.pid_gyro(45,150,precise_distance = False)
    ilan.turn(-30)
    ilan.pid_gyro(24,200,precise_distance = False)

    for k in range(2):
        ilan.pid_gyro(6,200,precise_distance = False)
        wait(500)
        ilan.pid_gyro(6,200,False,precise_distance = False)

    #שפיכת יחידות האנרגיה למשימה 

    ilan.pid_gyro(8,270,precise_distance = False)    
    # ilan.wait_for_button("test")

    #לקיחת יחידת האנרגיה וחזרה הביתה

    ilan.speed_formula(30,400,False)
    ilan.turn(30)
    ilan.pid_gyro(47,300,False,precise_distance = False)


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




TEXT_MENU = """Choose Run: 
 ^ - Scroll UP Runs
 > - Scroll UP Runs
   """



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
    run_time = 0

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

                run_time = Runs[current_run][1]()
            
                current_run += 1

                if current_run >= len(Runs):
                    current_run = 0

                wait(300)

                ilan.write("Last run: {} s \nTotal: {} s \n{}".format(round(run_time, 1), round(elsapsed_time.time()/1000.0, 1), Runs[current_run][0]))
        except Exception as EX :
            ilan.write("{}\nLast run: {} s \nTotal: {} s".format(str(EX), round(run_time, 1), round(elsapsed_time.time()/1000.0, 1)))
            wait(1500)
            
            

running()
