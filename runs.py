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
        # ilan.write("Run time: {} sec.".format(round(total_time, 1)))
        return result
    return timeit_wrapper


ilan = Robot()

##### Center Run #####


@timeit
def run_1():

        """מבצע את משימות M07,M15"""

        #  ביצוע משימה M15
        # 2023-01-18 rtm changed the run - added slide in front of arm. More accurate - so reduced 4->3 times push

        ilan.pid_gyro(16,precise_distance = False)
        ilan.turn(-45)
        ilan.speed_formula(52,500)
            
        # התיישרות על משימה M14

        ilan.turn(90)

        # ilan.pid_gyro(8,Forward_Is_True = False,precise_distance = False)

        ilan.pid_gyro(10,precise_distance = False)

        ilan.drive_by_seconds(200, 2)
        wait(300)
        ilan.pid_gyro(11.95,200,Forward_Is_True = False,precise_distance = False)

        #  ביצוע משימה M15
        for i in range (3):
            ilan.pid_gyro(11.95 + i,200,precise_distance = False)
            wait(700)
            ilan.pid_gyro(11.95,200,Forward_Is_True = False,precise_distance = False)

        # חזרה הביתה

        ilan.pid_gyro(5,400,Forward_Is_True =  False,precise_distance = False)
        ilan.turn(90,200)
        ilan.pid_gyro(58,400,precise_distance = False)



@timeit
def run_2():

    """מבצע את משימות M08,M14"""

    #  ביצוע משימה M08 

    ilan.speed_formula(47 ,400)
    ilan.speed_formula(51,500,False)

    # ביצוע משימה M14
    #2023-01-21 rtm Add wait for button so we can lower the alignment tool manually
    ilan.beep()
    ilan.wait_for_button("Before Turn",True)
    ilan.beep()
    ilan.turn(-52,200)
    ilan.speed_formula(48,400)
    # ilan.run_seconds(0.5,100)
        
    ilan.pid_gyro(2,100)

    # חזרה הביתה

    ilan.speed_formula(42,500,False)



@timeit
def run_3():

    """מבצע את M10 ועובר בתים"""

    #Worked well 14/1/23

    # נסיעה ל M10

    ilan.speed_formula(74,450)
    
    # הרמת המחסום האדום

    ilan.left_medium_motor.run_angle(400,-100)

    # שחרור יחידות האנרגיה 

    ilan.right_medium_motor.run_angle(350,110)
    
    # נסיעה לבית האדום ואסיפת יחידת אנרגיה

    ilan.right_medium_motor.run_angle(350,-10,wait = False)
    ilan.pid_gyro(90,500,precise_distance = False)



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
   # ilan.wait_for_button("60 - turn", debug)
    ilan.turn(-57)
    ilan.right_medium_motor.run_angle(1500,80,wait = False)
    ilan.pid_gyro(17,precise_distance = False)
    # ilan.right_medium_motor.run_angle(-200,90)
    ilan.right_medium_motor.run_until_stalled(-200, Stop.HOLD, duty_limit=60)

    # נסיעה על קו

    ilan.turn(-32)
    ilan.pid_gyro_until_color_in_one_sensor()
    ilan.pid_follow_line_until_other_detect_color(1,ilan.color_sensor_left,ilan.color_sensor_right,125,False,stop_color = Color.BLACK)

    # אסיפת יחידת האנרגיה האחרונה ממשימה M04

    ilan.turn(65)
    ilan.speed_formula(30,250,False)

    # חזרה הביתה

    ilan.turn(30)
    ilan.pid_gyro(2,precise_distance = False)
    ilan.turn(30)
    ilan.pid_gyro(105,600,precise_distance = False)



@timeit
def run_5(): 

    """ביצוע משימה M03"""

    #נסיעה לM03

    ilan.pid_gyro(42,150,precise_distance = False)
    ilan.turn(-30)
    ilan.pid_gyro(22,200,precise_distance = False)

    #שפיכת יחידות האנרגיה למשימה 

    ilan.pid_gyro(8,270,precise_distance = False)
    # ilan.wait_for_button("sdd", True)
    # wait(500)
    

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
