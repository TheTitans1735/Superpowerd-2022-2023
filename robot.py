#!/usr/bin/env pybricks-micropython

import csv
import time

from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.media import ev3dev
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

#import datetime
"""
All Robot actions
"""
class Robot:

    ##### ROBOT TRAITS #####
    
    def __init__(self):

        # define robot
        self.ev3 = EV3Brick()

        ## Ilan's Configuration ##
        # motors
        self.left_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)

        # robot
        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter=62.4, axle_track=122)
        self.robot.settings(straight_speed=200, straight_acceleration=100, turn_rate=100)

        # color sensors
        self.color_sensor_left = ColorSensor(Port.S2)
        self.color_sensor_right = ColorSensor(Port.S1)

        # gyro sensor
        self.gyro_sensor= GyroSensor(Port.S3)

        # wall's motors
        self.wall_x_motor = Motor(Port.D) 
        self.wall_y_motor = Motor(Port.A,Direction.COUNTERCLOCKWISE) 

        # define constant traits - wall's max angles
        self.WALL_MAX_ANGLE_X = 860
        self.WALL_MAX_ANGLE_Y = 740
        


    ##### RESET WALL #####

    def reset_wall(self):
        """"
        מאפס את הקיר לצד שמאל למטה
        """

        # define x & y motor's speed
        speed_x = -800
        speed_y = -1200

        # move the wall to max values
        self.wall_y_motor.run_until_stalled(speed_y,Stop.HOLD, duty_limit=75)
        self.wall_x_motor.run_until_stalled(speed_x,Stop.HOLD, duty_limit=15)
        wait(100)

        # make wall's 0 angle current angle
        self.wall_x_motor.reset_angle(0)
        self.wall_y_motor.reset_angle(0)

        # enter the current wall values into the file
        self.push_wall_values()
        
        # write current angles
        self.write("x = " + str(self.wall_x_motor.angle()) + "\ny = " + str(self.wall_y_motor.angle()))



    ##### RESET WALL BOTTON RIGHT #####

    def reset_wall_bottom_right(self):
        """"
        מאפס את הקיר לצד ימין למטה
        """

        # define x & y motor's speed
        speed_x = 800
        speed_y = -1200
        
        # move the wall to max values
        self.wall_y_motor.run_until_stalled(speed_y,Stop.HOLD, duty_limit=75)
        self.wall_x_motor.run_until_stalled(speed_x,Stop.HOLD, duty_limit=15)
        wait(100)

        # make wall's 0 angle current angle
        self.wall_x_motor.reset_angle(self.WALL_MAX_ANGLE_X)
        self.wall_y_motor.reset_angle(0)

        # enter the current wall values into the file
        self.push_wall_values()
        
        # write current angles
        self.write("x = " + str(self.wall_x_motor.angle()) + "\ny = " + str(self.wall_y_motor.angle()))
            

        
    ##### UPDATE WALL'S CURRENT VALUES #####

    def update_angles_from_file(self):
        """
        עדכון ערך הפוזיציה הנוכחית של הקיר לפי מה שנכתב בקובץ הטקסט
        """

        # with open('wall_values.txt') as f:
        #     content = f.readline()

        #     x_value, y_value = content.split(",")
        #     wait(50)

        #     self.wall_x_motor.reset_angle(int(x_value))
        #     self.wall_y_motor.reset_angle(int(y_value))

        pass



    ##### PUSH WALL'S CURRENT VALUES #####

    def push_wall_values(self):
        """
        כתיבת ערך הפוזיציה הנוכחית של הקיר בקובץ טקסט    
        """
        # with open('wall_values.txt', 'w+') as f:
        #     wait(50)
        #     f.write(str(self.wall_x_motor.angle()) + "," + str(self.wall_y_motor.angle()))

        pass
    
    

    ##### MOVE WALL TO POINT #####

    def move_wall_to_point(self, x:int,y:int, speed=-1200, x_wait = True, y_wait = True):
        """
        הזזת הקיר לנקודה מסויימת בטווח התנועה שלו
        """
        # get the wall's current position from file
        self.update_angles_from_file()

        # make sure wall does not try to extend beyond boundries:
        # define minimum and maximum values
        x = min( x, self.WALL_MAX_ANGLE_X)
        y = min( y, self.WALL_MAX_ANGLE_Y)
        x = max( x, 10)
        y = max( y, 10)
        
        # move motors until wall reaches the target position
        # motors can move together or continue to next function based on wait paremiter 
        self.wall_x_motor.run_target(speed, x, Stop.BRAKE, wait = x_wait)
        self.wall_y_motor.run_target(speed, y, Stop.BRAKE, wait = y_wait) 
        
        

        # print current wall values
        print("x = " + str(self.wall_x_motor.angle()) + ", y = "  + str(self.wall_y_motor.angle()))
        


    ##### MEASURE WALL MAX VALUES #####

    def measure_wall_max_values(self):
        """"
        פונקציה שבעזרתה בדקנו מה האיקס והוואי של הקיר בפינות
        """

        self.reset_wall()

        # run the motor to extreme
        max_x = self.wall_x_motor.run_until_stalled(800,Stop.HOLD, duty_limit=20)
        max_y = self.wall_y_motor.run_until_stalled(800,Stop.HOLD, duty_limit=1)

        self.wall_y_motor.stop()
        self.wall_x_motor.stop()

        # print current wall values
        self.write("max x= " + str(max_x) + " max y= " + str(max_y))



    ##### PID Gyro #####

    def pid_gyro(self, Td, Ts = 150, Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02):
        """
        PID Gyro נסיעה ישרה באמצעות מנגנון
        """

        direction_indicator = -1
        speed_indicator = -1       #משתנה שנועד כדי לכפול אותו במהירות ובתיקון השגיאה כדי שנוכל לנסוע אחורה במידת הצורך     

        if Forward_Is_True:             #אם נוסעים קדימה - תכפול באחד. אחורה - תכפול במינוס אחד
            direction_indicator = -1
            speed_indicator = 1   

        # reset
        self.robot.reset() 
        self.gyro_sensor.reset_angle(0)

        # Td = 1000 # target distance
        # Ts = 150 # target speed of robot in mm/s

        # Kp = 3.06 #  the Constant 'K' for the 'p' proportional controller
        # Ki = 0.027 #  the Constant 'K' for the 'i' integral term
        # Kd = 3.02 #  the Constant 'K' for the 'd' derivative term

        # initialize
        integral = 0 
        derivative = 0 
        lastError = 0 

        ## Start Loop ##
        while (abs(self.robot.distance()) < Td * 10):
            wait(20) #ע"מ לא לגזול את כל המשאבים
            self.check_forced_exit()

            # P - Proportional
            # תיקון השגיאה המיידית
            # הגדר את השגיאה כזווית הנוכחית של הג'יירו
            error = self.gyro_sensor.angle() 

            print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))

            # I - Integral
            # תיקון השגיאה המצטברת
            # אם ישנה שגיאה, הוסף אותה לאינטגרל
            if (error == 0):
                integral = 0

            else:
                integral = integral + error    

            # D - Derivative
            # תיקון השגיאה העתידית
            # הגדר את הדריבטיב כשגיאה הנוכחית - השגיאה האחרונה
            derivative = error - lastError  
            
            # הגדרת זווית הפנייה הדרושה בנסיעה
            # הכפלת כל חלק במשקל התיקון שלו
            correction = (Kp * (error) + Ki * (integral) + Kd * derivative) * -1

            # נסיעה לפי המהירות וזווית הנסיעה של התיקון
            self.robot.drive(Ts * speed_indicator , correction * direction_indicator * -1)

            # הגדר את השגיאה האחרונה כשגיאה הנוכחית
            lastError = error  
        
        # עצור את הרובוט
        self.robot.stop()



    ##### PID GYRO WHILE MOVE WALL #####

    def PID_while_move_wall(self, x:int, y:int, drive_distance, drive_speed = 150, seconds_to_start_wall = 0, wall_speed =- 1200,
                            Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02):
        """
        PID Gyro הזזת הקיר תוך כדי נסיעה
        """
        
        self.update_angles_from_file()

        # define minimum and maximum wall values
        x = min( x, self.WALL_MAX_ANGLE_X)
        y = min( y, self.WALL_MAX_ANGLE_Y)
        x = max( x, 10)
        y = max( y, 10)
        # add 10 because y axis might get stuck while going down
        

        ## PID Gyro Part ##

        direction_indicator = -1
        speed_indicator = -1       #משתנה שנועד כדי לכפול אותו במהירות ובתיקון השגיאה כדי שנוכל לנסוע אחורה במידת הצורך   

        if Forward_Is_True:             #אם נוסעים קדימה - תכפול באחד. אחורה - תכפול במינוס אחד
            direction_indicator = -1
            speed_indicator = 1   

        # reset
        self.robot.reset() 
        self.gyro_sensor.reset_angle(0)

        # Td = 1000 # target distance
        # Ts = 150 # target speed of robot in mm/s

        # Kp = 3 #  the Constant 'K' for the 'p' proportional controller
        # Ki = 0.025 #  the Constant 'K' for the 'i' integral term
        # Kd = 3 #  the Constant 'K' for the 'd' derivative term

        # initialize
        integral = 0 
        derivative = 0 
        lastError = 0 

        # start stopwatch to use if user wants to start moving the wall a couple seconds after starting to drive
        sw_for_wall_timing = StopWatch()

        ## Start Loop ##
        while (abs(self.robot.distance()) < drive_distance * 10 or self.wall_x_motor.speed() != 0 and self.wall_y_motor.speed() != 0):
            self.check_forced_exit()

            # P - Proportional
            # תיקון השגיאה המיידית
            # הגדר את השגיאה כזווית הנוכחית של הג'יירו
            error = self.gyro_sensor.angle() 

            print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))

            # I - Integral
            # תיקון השגיאה המצטברת
            # אם ישנה שגיאה, הוסף אותה לאינטגרל
            if (error == 0):
                integral = 0

            else:
                integral = integral + error    

            # D - Derivative
            # תיקון השגיאה העתידית
            # הגדר את הדריבטיב כשגיאה הנוכחית - השגיאה האחרונה
            derivative = error - lastError  
            
            # הגדרת זווית הפנייה הדרושה בנסיעה
            # הכפלת כל חלק במשקל התיקון שלו
            correction = (Kp * (error) + Ki * (integral) + Kd * derivative) * -1

            # נסיעה לפי המהירות וזווית הנסיעה של התיקון
            self.robot.drive(drive_speed * speed_indicator , correction * direction_indicator * -1)

            # הפעלת הקיר (במקרה שהזמן להמתנה להפעלת הקיר עבר)
            if sw_for_wall_timing.time() > seconds_to_start_wall * 1000: 
                self.wall_x_motor.run_target(wall_speed, x, Stop.BRAKE, wait = False)     
                self.wall_y_motor.run_target(wall_speed, y, Stop.BRAKE, wait = False)
            
            # הגדרת השגיאה האחרונה כשגיאה הנוכחית
            lastError = error  
        
        # עצירת הרובוט והקיר          
        self.robot.stop()
        self.wall_x_motor.stop()
        self.wall_y_motor.stop()

        self.push_wall_values()

        # במקרה והנסיעה הסתיימה לפני שהזזת הקיר הושלמה, הזז את הקיר לנקודה הרצוייה
        if self.wall_x_motor.angle() != x or self.wall_y_motor.angle() != y:                
            self.move_wall_to_point(x, y)

        # הדפסת נתוני הנסיעה וערכי הקיר הנוכחיים
        print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))
        print("wall_x: " + str(self.wall_x_motor.angle()) + " wall_y: " + str(self.wall_y_motor.angle()))
        


        
    ##### PID GYRO UNTIL COLOR #####

    def pid_gyro_until_color(self, stop_color = Color.BLACK, Ts = 150, Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02):
        """
        PID Gyro נסיעה ישרה עד זיהוי קו באמצעות
        """
        
        direction_indicator = -1
        speed_indicator = -1       #משתנה שנועד כדי לכפול אותו במהירות ובתיקון השגיאה כדי שנוכל לנסוע אחורה במידת הצורך  

        if Forward_Is_True:             #אם נוסעים קדימה - תכפול באחד. אחורה - תכפול במינוס אחד
            direction_indicator = -1
            speed_indicator = 1   

        # reset
        self.robot.reset() 
        self.gyro_sensor.reset_angle(0)

        # Td = 1000 # target distance
        # Ts = 150 # target speed of robot in mm/s

        # Kp = 3 #  the Constant 'K' for the 'p' proportional controller
        # Ki = 0.025 #  the Constant 'K' for the 'i' integral term
        # Kd = 3 #  the Constant 'K' for the 'd' derivative term

        # initialize
        integral = 0 
        derivative = 0 
        lastError = 0 

        while (self.color_sensor_right.color() != stop_color or self.color_sensor_left.color() != stop_color):
            self.check_forced_exit()

            # P - Proportional
            # תיקון השגיאה המיידית
            # הגדר את השגיאה כזווית הנוכחית של הג'יירו
            error = self.gyro_sensor.angle() 

            print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))

            # I - Integral
            # תיקון השגיאה המצטברת
            # אם ישנה שגיאה, הוסף אותה לאינטגרל
            if (error == 0):
                integral = 0

            else:
                integral = integral + error    

            # D - Derivative
            # תיקון השגיאה העתידית
            # הגדר את הדריבטיב כשגיאה הנוכחית - השגיאה האחרונה
            derivative = error - lastError  
            
            # הגדרת זווית הפנייה הדרושה בנסיעה
            # הכפלת כל חלק במשקל התיקון שלו
            correction = (Kp * (error) + Ki * (integral) + Kd * derivative) * -1

            # נסיעה לפי המהירות וזווית הנסיעה של התיקון
            self.robot.drive(Ts * speed_indicator , correction * direction_indicator * -1)

            # הגדר את השגיאה האחרונה כשגיאה הנוכחית
            lastError = error  
        
        # עצור את הרובוט
        self.robot.stop()



    ##### RUN STRAIGHT ####

    def run_straight (self, distance):
        """
        נסיעה ישרה לפי סנטימטרים
        """
        self.robot.straight(distance * 10)


    ##### PID Follow Line #####

    def pid_follow_line(self, distance, speed, line_sensor, stop_condition = lambda: False, Kp = 1.30 ,Ki = 0.01, white_is_right = True, Kd=0.07):
        """
        PID מעקב אחרי קו עם מנגנון 
        """

        self.robot.reset() 

        # define gyro angle robot starts driving in
        initial_gyro_angle = self.gyro_sensor.angle()

        # Start a stopwatch to measure elapsed time
        watch = StopWatch()

        ## Following code was remarked for it is only needed when learning the PID values ##

        #log_file_name = time.strftime("%Y_%m_%d_%H_%M_%S")
        # print file's name
        #print(log_file_name)
        #self.data =DataLog("Distance", "Reflection", "Error", "PROPORTIONAL_GAIN", "INTEGRAL_GAIN", "DERIVATIVE_GAIN", "integral", "derivative", "turn_rate", "gyro", "speed", "white_is_right","Gyro_Offset","MS_From_Start",name=log_file_name,timestamp=False)
        
        # Calculate the light threshold. Choose values based on your measurements.
        BLACK = 6
        WHITE = 71

        threshold = (BLACK + WHITE) / 2

        # set drive speed as speed of paremeter
        DRIVE_SPEED = speed

        # Set the gain of the proportional line controller. This means that for every
        # percentage point of light deviating from the threshold, we set the turn
        # rate of the drivebase to 1.2 degrees per second.
        # For example, if the light value deviates from the threshold by 10, the robot
        # steers at 10*1.2 = 12 degrees per second.

        PROPORTIONAL_GAIN = Kp
        DERIVATIVE_GAIN = Kd
        INTEGRAL_GAIN = Ki

        integral = 0
        derivative =0
        last_error = 0
        arr_results = []

        ## Follow The Line Until Target Distance is Reached ##
        while (abs(self.robot.distance()) < distance * 10):
            self.check_forced_exit()

            # Calculate the deviation from the threshold
            error = line_sensor.reflection() - threshold # P
            integral = integral + error # I
            derivative = error - last_error # D
            
            # Calculate the turn rate.
            turn_rate = PROPORTIONAL_GAIN * error + DERIVATIVE_GAIN * derivative + INTEGRAL_GAIN * integral

            # white is right - when following the line, you may follow the right side of the black line or the left side of it.
            # based on that, change the turn rate of driving on the line
            if white_is_right:
                turn_rate = turn_rate * -1

            # Set the drive base speed and turn rate.
            self.robot.drive(DRIVE_SPEED, turn_rate)

            print("distance = " , self.robot.distance() , "  |  reflection = " , line_sensor.reflection() , "  |  error = " , error ,
                "  |  integral = " , integral , "  |  derivative = " , derivative , "  |  turn_rate = " , turn_rate, "  |  gyro = ", self.gyro_sensor.angle())
            
            # define the last error as current error
            last_error = error

            ## Following code was remarked for it is only needed when learning the PID values ##

            # log the driving data into the file
            # self.data.log(self.robot.distance(), line_sensor.reflection(), error, PROPORTIONAL_GAIN, INTEGRAL_GAIN, DERIVATIVE_GAIN,
            #               integral, derivative, turn_rate, self.gyro_sensor.angle(), speed, white_is_right,
            #               self.gyro_sensor.angle() - initial_gyro_angle,watch.time())

            # Save run data in array and add to an array of arrays which will be the function return value
            arr_result = self.robot.distance(), line_sensor.reflection(), error, PROPORTIONAL_GAIN, INTEGRAL_GAIN, DERIVATIVE_GAIN,integral, derivative, turn_rate, self.gyro_sensor.angle(), speed, white_is_right, self.gyro_sensor.angle() - initial_gyro_angle,watch.time()
            arr_results.append(arr_result)
            
            # עוצר במקרה שזיהה תנאי עצירה
            if stop_condition():
                break

            # You can wait for a short time or do other things in this loop.
            wait(10)
            
        # stop robot movement
        self.robot.stop()

        return arr_results



    ##### CREATE LOG FILE #####

    def create_log_file(self):
        """
        יצירת קובץ למדידת ערכי פיד אופטימליים
        """
        
        log_file_name = time.strftime("%Y_%m_%d_%H_%M_%S")

        # print file's name
        print(log_file_name)

        # Create the file to write in with following catagories:
        # Distance | Reflection | Error | Proportional Gain | Integral Gain | Derivative Gain | Integral | Derivative |
        # Turn Rate | Gyro | Speed | Side of the Line | Gyro Offset | Time From Start |

        self.data = DataLog("Distance", "Reflection", "Error", "PROPORTIONAL_GAIN", "INTEGRAL_GAIN", "DERIVATIVE_GAIN", "integral", "derivative", "turn_rate", "gyro", "speed", "white_is_right","Gyro_Offset","MS_From_Start",name=log_file_name,timestamp=False)
    


    ##### WRITE TO LOG FILE #####

    def write_to_log_file(self, message):
        """
        כתיבה לתוך הקובץ שנוצר בפונקציה הקודמת
        """

        for a in message:
            self.data.log(a)



    ##### LEARN THE BEST VALUES FOR PID FOLLOW LINE #####

    def learn_pid_line_values_2022_03_11 (self, distance = 150, speed = 100, value_checking = "Kp", kp = 1.3, ki = 0.01, kd = 0.07, num_of_loops = 20):
        """
        פונקציה ללמידת ערכי הפיד האופטימליים למעקב אחרי קו     
        """

        # איפוס הקיר והזזתו למרכז - למעלה (על מנת שלא ישפיע על הנסיעה)
        self.reset_wall()
        self.move_wall_to_point(self.WALL_MAX_ANGLE_X / 2, self.WALL_MAX_ANGLE_Y)

        # שימוש בפונקציית יצירת הקובץ
        self.create_log_file()

        # הגדרת הערך ההתחלתי, הסופי והכמות שרוצים להגדיל אותו בכל סיבוב
        loop_start_value = 0.01
        loop_end_value = 0.03
        loop_step_size = 0.002

        loop_current_value = loop_start_value

        # הכנסת הערכים שהוגדרו אל המשתנה אותו אנו רוצים לבדוק
        if value_checking == "Kp" or value_checking == "kp":
            kp = loop_start_value

        elif value_checking == "Ki" or value_checking == "ki":
            ki = loop_start_value

        elif value_checking == "Kd" or value_checking == "kd":
            kd = loop_start_value


        ## הלולאה ##
        while loop_current_value < loop_end_value:
            
            # איפוס חיישן הג'יירו
            self.gyro_sensor.reset_angle(0)

            # הפעלת הפונקציה וכתיבת התוצאות בתוך הקובץ שנוצר
            follow_line_results = self.pid_follow_line(distance, speed, self.color_sensor_right, Kp = kp, Ki = ki, Kd = kd)
            self.write_to_log_file(follow_line_results)
            
            # הגדלת הערכים
            if value_checking == "Kp" or value_checking == "kp":
                kp = kp + loop_step_size

            elif value_checking == "Ki" or value_checking == "ki":
                ki = ki + loop_step_size

            elif value_checking == "Kd" or value_checking == "kd":
                kd = kd + loop_step_size

            loop_current_value += loop_step_size

            # המתנה שהמריץ ייקח את הרובוט חזרה אל תחילת הקו
            wait(5000)



    ##### PID FOLLOW RIGHT LINE UNTIL LEFT DETECT COLOR #####

    def pid_follow_line_until_other_detect_color (self, lines_till_stop, follow_color_sensor, detection_color_sensor,
                                                    speed = 90, white_is_right = True, stop_color = Color.BLACK, kp = 1.3, ki = 0.01, kd = 0.07):
        """
        סע על הקו השחור עד זיהוי כמות מסויימת של קווים שחורים עם חיישן הצבע השני
        """
        
        my_debug = False

        # מגדיר את תנאי העצירה
        stop_on_black = lambda : detection_color_sensor.color() == stop_color

        self.wait_for_button("Start Follow", my_debug)

        # מוצא קווים ככמות הפרמטר
        for i in range (0, lines_till_stop):
            self.check_forced_exit()
            
            if (i > 0):
                # לאחר מציאת קו, סע 10 ס"מ במהירות נמוכה יותר כדי
                # להתרחק מן הקו ולהיות בטוח מפני פניות
                self.pid_follow_line(10, 80, follow_color_sensor, Kp=kp, white_is_right = white_is_right)
            
            # נסיעה עד זיהוי תנאי העצירה - זיהוי הקו השחור
            self.pid_follow_line(150, speed, follow_color_sensor, stop_condition = stop_on_black, Kp = kp, white_is_right = white_is_right, Ki = ki, Kd = kd)
            self.beep()
    
    
    
    ##### STRAIGHTEN ON BLACK #####

    def straighten_on_black(self, speed = 90, drive_forward = True):
        """
        התיישרות על קו שחור
        """
        
        # הגדרת המהירות בהתאם לרצון לנסוע קדימה / אחורה
        if drive_forward == False:
            speed = speed * -1

        # התחלת הנסיעה
        self.right_motor.run(speed)
        self.left_motor.run(speed)

        right_sensor_flag = False
        left_sensor_flag = False
        target_reflection = -1

        ## התיישרות על הקו ##
        ## כל עוד שני החיישנים עוד לא זיהו שחור ##
        while (right_sensor_flag == False or left_sensor_flag == False):
            self.check_forced_exit()

            # אם הרובוט עוד לא זיהה שחור באחד החיישנים
            if target_reflection == -1:

                # אם החיישן הימני מזהה שחור
                if self.color_sensor_right.color() == Color.BLACK:
                    right_sensor_flag = True

                    # הגדרת האור המוחזר הרצוי כאור שהחיישן הימני קולט
                    target_reflection = self.color_sensor_right.reflection()
                    self.right_motor.brake()

                # אם החיישן השמאלי מזהה שחור
                elif self.color_sensor_left.color() == Color.BLACK:
                    left_sensor_flag = True

                    # הגדרת האור המוחזר הרצוי כאור שהחיישן השמאלי קולט
                    target_reflection = self.color_sensor_left.reflection()
                    self.left_motor.brake()

                # הדפסת הצבע שהחיישנים קולטים
                self.write("L: " + str(self.color_sensor_left.color()) + " R: " + str(self.color_sensor_right.color()))

            # אם אחד מהחיישנים זיהה צבע שחור
            else:

                # אם החיישן הימני זיהה שחור
                if self.color_sensor_right.reflection() == target_reflection:
                    right_sensor_flag = True

                    # עצור את המנוע הימני
                    self.right_motor.brake()

                # אם החיישן השמאלי זיהה שחור
                if self.color_sensor_left.reflection() <= target_reflection:
                    left_sensor_flag = True

                    # עצור את המנוע השמאלי
                    self.left_motor.brake()

                # הדפסת האור שמוחזר בשני החיישנים
                self.write("L: " + str(self.color_sensor_left.reflection()) + " R: " + str(self.color_sensor_right.reflection()))

            wait(10)
        
        # הדפסת האור והצבע ששני החיישנים קוראים
        self.write("C Left: " + str(self.color_sensor_left.color()))
        self.write("C Right: " + str(self.color_sensor_right.color()))
        self.write("R Left: " + str(self.color_sensor_left.reflection()))
        self.write("R Right: " + str(self.color_sensor_right.reflection()))



    ##### RUN STRAIGHT ####

    def run_straight (self, distance):
        self.robot.straight(distance * 10)



    ##### TURN #####

    def turn (self, angle, speed=100):
        # איפוס חיישן הג'יירו
        self.gyro_sensor.reset_angle(0)
        wait(10)

        ## פנייה ימינה - זווית פנייה חיובית ##
        if angle > 0:


            # נוסע כמעט עד ערך הזווית במהירות מלאה
            while self.gyro_sensor.angle() <= angle * 0.8:
                self.check_forced_exit()

                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות מלאה
                self.right_motor.run(speed = (-1 * speed))
                self.left_motor.run(speed = speed)

            # עצירת מנועי הרובוט
            self.right_motor.brake()
            self.left_motor.brake()


            #נוסע את שארית ערך הזווית במהירות מופחתת פי 0.2
            while self.gyro_sensor.angle() < angle:
                self.check_forced_exit()

                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות כמעט מלאה
                self.right_motor.run(speed = (-0.2 * speed))
                self.left_motor.run(speed = speed * 0.2)

            # עצירת מנועי הרובוט
            self.right_motor.brake()
            self.left_motor.brake()
            

            #  תיקון איטי נוסף במקרה הצורך
            while self.gyro_sensor.angle() > angle:
                self.check_forced_exit()
                
                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות נמוכה מאוד
                self.right_motor.run(20)
                self.left_motor.run(-20)
                
                wait(10)



        ## פנייה שמאלה - זווית פנייה שלילית ##
        elif angle < 0:  
            
            
            # נוסע כמעט עד ערך הזווית במהירות מלאה, הגלגלים נעים בכיוון הפוך 
            while self.gyro_sensor.angle() >= angle * 0.8:
                self.check_forced_exit()
                
                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות מלאה
                self.right_motor.run(speed=(speed))
                self.left_motor.run(speed=speed*-1)

            # עצירת מנועי הרובוט
            self.right_motor.brake()
            self.left_motor.brake()


            # נוסע את שארית ערך הזווית במהירות מופחתת פי 0.2
            while self.gyro_sensor.angle() > angle:
                self.check_forced_exit()

                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות כמעט מלאה
                self.right_motor.run(speed=(0.2 * speed))
                self.left_motor.run(speed=speed*-0.2)

            # עצירת מנועי הרובוט
            self.right_motor.stop()
            self.left_motor.stop()


            # תיקון איטי נוסף במקרה הצורך
            while self.gyro_sensor.angle() > angle:
                self.check_forced_exit()

                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות איטית מאוד
                self.right_motor.run(-20)
                self.left_motor.run(20)

                wait(10)  


        # לאחר הפנייה, עצור את מנועי הרובוט
        self.right_motor.stop()
        self.left_motor.stop()

        # הדפסת הזווית הסופית
        print("final degree: " + str(self.gyro_sensor.angle()))



    ##### TURN UNTIL SECONDS ####

    def turn_until_seconds(self, seconds, max_angle, speed = 150, turn_right = True):
        """Right = True, Left = False"""

        # שנה את מהירות הפנייה בהתאם לרצון המשתמש לפנות ימינה או שמאלה
        if turn_right == False:
            speed = speed * -1

        # הפעל שעון עצר
        sw = StopWatch()

        # איפוס חיישן הג'יירו
        self.gyro_sensor.reset_angle(0)
        
        ## הפנייה ##
        # פנייה עד כמות השניות / עד הגעה לזווית רצויה
        while sw.time() < seconds * 1000 and abs(self.gyro_sensor.angle()) < max_angle:
            self.check_forced_exit()
            
            # הפעלת המנועים
            self.left_motor.run(speed)
            self.right_motor.run(speed * -1)

        # עצירת המנועים
        self.right_motor.stop()
        self.left_motor.stop()



    ##### TURN TO THRESHOLD #####

    def turn_to_threshold (self, line_sensor, turn_right = True, speed = 25):

        # שנה את מהירות הפנייה בהתאם לרצון המשתמש לפנות ימינה או שמאלה
        if turn_right == False:
            speed = speed * -1

        ## הפנייה ##
        # פנייה עד זיהוי הצבע השחור
        while line_sensor.reflection() > 40:
            self.check_forced_exit()
            
            # הפעלת המנועים
            self.left_motor.run(speed)
            self.right_motor.run(speed * -1)

        # עצירת המנועים
        self.right_motor.brake()
        self.left_motor.brake()

        
        
    ##### CHECK GYRO #####

    def check_gyro(self):
        """
        פונקציה לבדיקה האם הגיירו מאופס, אם לא משמיע אזעקה עד שהוא מאופס.
        """
    
        try:
            current_gyro = self.gyro_sensor.angle()
            wait(500)

            while current_gyro != self.gyro_sensor.angle():

                for _ in range(3):

                    self.ev3.speaker.play_file("GENERAL_ALERT.wav")
                    wait(10)

                wait(10)

        except:
            self.ev3.speaker.play_file("GENERAL_ALERT.wav")
            wait(10)
            
        return True



    ##### CHECK FORCED EXIT #####

    def check_forced_exit(self):
        """
        במקרה שנלחצים שני כפתורים בו זמנית, הפעל שגיאה
        """

        if len(self.ev3.buttons.pressed()) >= 2:

            self.write("Forced Exit")
            print("!!!!!!!!!!!!!!!!!!!! FORCED EXIT !!!!!!!!!!!!!!!!!!!!!!!!")
            raise Exception("Forced Exit")
        


    ##### WAIT FOR BUTTON #####

    def wait_for_button(self, text, debug = True):
        """
        מחכה לכפתור וכותב טקסט - Debugging מנגנון
        """
        
        # הדפסת הטקסט הנתון
        self.write(text)
        self.check_forced_exit()
        
        if not debug:
            return
        
        # חכה ללחיצת כפתור
        while not any(self.ev3.buttons.pressed()):
            wait(10)
                


    ##### WRITE ON EV3 SCREEN #####

    def write(self, my_text):
        """
        הדפסת טקסט נתון במחשב ועל מסך הרובוט
        """

        # נקה את מסך הרובוט
        self.ev3.screen.clear()

        # הדפסת הטקסט במחשב
        print(my_text)
        
        # \n הפרד את הטקסט לשורות נפגדות לפי
        lines = my_text.split("\n")

        # הדפסת הטקסט על מסך הרובוט עם מרווחים בין כל שורה
        for i in range(0, len(lines)):
            self.ev3.screen.draw_text(1, i * 20, lines[i], text_color = Color.BLACK, background_color=None)
    


    ##### BEEP #####

    def beep(self):
        """"
        אילן עושה ביפ
        """

        self.ev3.speaker.beep()

    

    ##### SAY TEXT #####

    def say(self, text, voice='m1', volume = 100):
        """"
        אילן אומר את הטקסט
        ניתן לשלוט על הווליום ואפילו לשנות את המבטא של אילן
        """
        
        # הגדרת הווליום של הבקר
        self.ev3.speaker.set_volume(volume)

        # הגדרת קול ההקראה
        self.ev3.speaker.set_speech_options(voice)

        # הבקר מקריא את הטקסט
        self.ev3.speaker.say(text)


##### The End :) #####