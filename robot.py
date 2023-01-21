#!/usr/bin/env pybricks-micropython

import csv


from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.media import ev3dev
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import time
# import datetime
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
        self.left_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
        self.right_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)

        # robot
        self.robot = DriveBase(self.left_motor, self.right_motor, wheel_diameter=62.4, axle_track=75)
        self.robot.settings(straight_speed=80, straight_acceleration=40, turn_rate=100)

        # color sensors
        self.color_sensor_left = ColorSensor(Port.S1)
        self.color_sensor_right = ColorSensor(Port.S2)

        # gyro sensor
        self.gyro_sensor= GyroSensor(Port.S3)

        # medium motors
        self.left_medium_motor = Motor(Port.B) 
        self.right_medium_motor = Motor(Port.A) 

        
        


    ##### RE



    def drive_by_seconds(self, speed, time_seconds):
        import time
        self.gyro_sensor.reset_angle(0)
        direction_indicator=1
        if (speed < 0):
            direction_indicator = -1 #אם נוסעים אחורה תתקן גיירו לצד השני 
        start = time.time()
        while ((time.time() - start) < time_seconds):
            print("gyro: " + str(self.gyro_sensor.angle()))
            self.robot.drive(speed, self.gyro_sensor.angle() * direction_indicator)
        self.robot.stop()



    ##### UPDATE WALL'S CURRENT VALUES #####

    def update_angles_from_file(self):
        """
        עדכון ערך הפוזיציה הנוכחית של הקיר לפי מה שנכתב בקובץ הטקסט
        """

        # with open('wall_values.txt'x  ) as f:
        #     content = f.readline()

        #     x_value, y_value = content.split(",")
        #     wait(50)

        #     self.wall_x_motor.reset_angle(int(x_value))
        #     self.wall_y_motor.reset_angle(int(y_value))

        pass



    ##### PUSH WALL'S CURRENT VALUES #####pass
    
    

    ##### MOVE WALL TO POINT #####

    

    ##### PID Gyro #####


    # def drive_run_time(speed=150, time):
    #     datetime.time. 
    def speed_formula(self, Td, Vmax = 300, Forward_Is_True = True, Kp = 3.09, Ki= 0.027, Kd = 3.02, alternative_cond = lambda : True): 
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
        while (abs(self.robot.distance()) <Td * 10) and alternative_cond():
            X = self.robot.distance()
            wait(1) #ע"מ לא לגזול את כל המשאבים
            XdivD = abs(X) / (Td * 10.0)
            Ts = 4 * Vmax * (XdivD - (XdivD ** 2))
            if Ts < 20:
                Ts = 20
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
        self.left_motor.hold()
        self.right_motor.hold()
        print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))


    def rst_to_angle_zero(self):
        """מטרת פונקציה זו היא שהרובוט יתקן את עצמו בעזרת סיבוב לזווית 0"""
        while(self.gyro_sensor.angle() < 0):
            self.left_motor.run(30)
            self.right_motor.run(-30)
        while(self.gyro_sensor.angle() > 0):
            self.left_motor.run(-30)
            self.right_motor.run(30)
        self.robot.stop()

        
    def align_on_black_white(self,right_first):
        """מטרת פונקציה זו היא שהרובוט יתקן את עצמו בעצירה על קו"""
        speed = 50
        if right_first == True:
            while(self.color_sensor_right.color() == Color.BLACK):
                self.right_motor.run(-1 * speed)
                self.write("L: " + str(self.color_sensor_left.color()) + " R: " + str(self.color_sensor_right.color()))
                # self.write("L: " + str(self.color_sensor_left.reflection()) + " R: " + str(self.color_sensor_right.reflection()))
            self.right_motor.hold()


            while(self.color_sensor_left.color() == Color.BLACK):
                self.left_motor.run(-1 * speed)
                self.write("L: " + str(self.color_sensor_left.color()) + " R: " + str(self.color_sensor_right.color()))
                # self.write("L: " + str(self.color_sensor_left.reflection()) + " R: " + str(self.color_sensor_right.reflection()))
            self.left_motor.hold()

        else:
            while(self.color_sensor_left.color() == Color.BLACK):
                self.left_motor.run(-1 * speed)
                self.write("L: " + str(self.color_sensor_left.color()) + " R: " + str(self.color_sensor_right.color()))
                # self.write("L: " + str(self.color_sensor_left.reflection()) + " R: " + str(self.color_sensor_right.reflection()))
            self.left_motor.hold()


            while(self.color_sensor_right.color() == Color.BLACK):
                self.right_motor.run(-1 * speed)
                self.write("L: " + str(self.color_sensor_left.color()) + " R: " + str(self.color_sensor_right.color()))
                # self.write("L: " + str(self.color_sensor_left.reflection()) + " R: " + str(self.color_sensor_right.reflection()))
            self.right_motor.hold()

        self.robot.stop()

        
    def pid_gyro(self, Td, Ts = 150, Forward_Is_True = True, Kp = 3.1, Ki= 0.025, Kd =3.3, alternative_cond = lambda : True,precise_distance = True):
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
        while (abs(self.robot.distance()) <Td * 10) and alternative_cond():
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
        print("hi")
        # if Forward_Is_True:
        #     self.left_motor.stop()
        #     self.right_motor.stop()
        #     self.robot.stop()
            
        # else:
        #     self.left_motor.hold()
        #     self.right_motor.hold()
        #     self.robot.stop()
            
        self.robot.stop()
        
        self.left_motor.brake()
        self.right_motor.brake()

        print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))
         
        if precise_distance == False :
            return 
        wait(200) # כדי שאילן יגיע לעצירה מוחלטת לגמרי
        
        if Forward_Is_True:
            self.robot.straight(Td*10-self.robot.distance())
        else:                                                       ### תיקון הסטיה במרחק (אם אילן נסע פחות/יותר ממה שאמור)
            self.robot.settings(-80,40) 
            self.robot.straight((Td*10+self.robot.distance()))
        
        self.robot.stop()
        print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))
        self.rst_to_angle_zero() #תתקן את עצמך בסיבוב עד שאתה מגיע ל0 מעלות
        wait(200)
        self.robot.settings(80,40) 
        print("distance: " + str(self.robot.distance()) + " gyro: " + str(self.gyro_sensor.angle()))


        
    ##### PID GYRO UNTIL COLOR #####

    def  pid_gyro_until_color_in_one_sensor(self, stop_color = Color.BLACK, Ts = 150, Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02,):
        stop_if_one_black = lambda: self.color_sensor_right.color() != stop_color and self.color_sensor_left.color() != stop_color
        self.pid_gyro(100, alternative_cond=stop_if_one_black,precise_distance = False)

    def pid_gyro_until_color_in_two_sensor(self, stop_color = Color.BLACK, Ts = 150, Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02):
        stop_if_both_black = lambda: self.color_sensor_right.color() != stop_color or self.color_sensor_left.color() != stop_color
        self.pid_gyro(100, alternative_cond=stop_if_both_black,precise_distance = False)

    def pid_gyro_until_color1(self, stop_color = Color.BLACK, Ts = 150, Forward_Is_True = True, Kp = 3.06, Ki= 0.027, Kd = 3.02):
        """
        PID Gyro נסיעה ישרה עד זיהוי קו באמצעות
        """
        
        direction_indicator = 1
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

        while self.color_sensor_right.color() != stop_color or self.color_sensor_left.color() != stop_color:

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
        wait(2000)
        print(self.gyro_sensor.angle())
    ##### RUN STRAIGHT ####

    def run_straight (self, distance):
        """
        נסיעה ישרה לפי סנטימטרים
        """
        self.robot.straight(distance * 10)


    ##### PID Follow Line #####

    def pid_follow_line(self, distance, speed, line_sensor, stop_condition = lambda: False, Kp = 0.55 ,Ki = 0.01, white_is_right = True, Kd=0.07):
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
            wait(1)
            
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
                                                    speed = 90, white_is_right = True, stop_color = Color.BLACK, kp = 0.55, ki = 0.01, kd = 0.07):
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
        self.right_motor.stop()
        self.left_motor.stop()
    
    
    
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
        right_first = False
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
                    self.right_motor.hold()
                    right_first = True

                # אם החיישן השמאלי מזהה שחור
                elif self.color_sensor_left.color() == Color.BLACK:
                    left_sensor_flag = True

                    # הגדרת האור המוחזר הרצוי כאור שהחיישן השמאלי קולט
                    target_reflection = self.color_sensor_left.reflection()
                    self.left_motor.hold()

                # הדפסת הצבע שהחיישנים קולטים
                self.write("L: " + str(self.color_sensor_left.color()) + " R: " + str(self.color_sensor_right.color()))
                # self.write("L: " + str(self.color_sensor_left.reflection()) + " R: " + str(self.color_sensor_right.reflection()))

            # אם אחד מהחיישנים זיהה צבע שחור
            else:
                left_reflection = self.color_sensor_left.reflection()
                right_reflection = self.color_sensor_right.reflection()
                # אם החיישן הימני זיהה שחור
                if right_reflection <= target_reflection:
                    right_sensor_flag = True

                    # עצור את המנוע הימני
                    self.right_motor.hold()

                # אם החיישן השמאלי זיהה שחור
                if left_reflection <= target_reflection:
                    left_sensor_flag = True

                    # עצור את המנוע השמאלי
                    self.left_motor.hold()

                # הדפסת האור שמוחזר בשני החיישנים
                self.write("L: " + str(left_reflection) + " R: " + str(right_reflection) + " T: " + str(target_reflection))

            wait(1)
        self.align_on_black_white(right_first)

        # הדפסת האור והצבע ששני החיישנים קוראים
        #self.write("C Left: " + str(self.color_sensor_left.color()))
        #self.write("C Right: " + str(self.color_sensor_right.color()))
        self.write("R Left: " + str(self.color_sensor_left.reflection()))
        self.write("R Right: " + str(self.color_sensor_right.reflection()))



    ##### RUN STRAIGHT ####

    def run_straight (self, distance):
        self.robot.straight(distance * 10)

    # def detect_line_on_turn(self,left_sensor = True):
    #     if left_sensor == True :
    #         SensorColor = self.color_sensor_left.color()
    #     while SensorColor != Color.BLACK :
    #         self.turn_to_threshold() 



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
            # self.right_motor.brake()
            # self.left_motor.brake()


            #נוסע את שארית ערך הזווית במהירות מופחתת פי 0.2
            while self.gyro_sensor.angle() < angle:
                self.check_forced_exit()

                # הדפסת ערך הזווית הנוכחית
                print("degree: " + str(self.gyro_sensor.angle()))

                # פנייה במהירות כמעט מלאה
                speed *= 0.8
                if speed < 20:
                    speed = 20
                    
                self.right_motor.run(speed = (-1 * speed))
                self.left_motor.run(speed = speed)

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
        while line_sensor.Color() != Color.BLACK:
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

    def wait_for_button(self, text = "TEST", debug = True):
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
        


    def stop_on_line(self, color):
        while ColorSensor.reflection() != color:
            wait(1)            
        self.robot.stop()


        
    def gyro_reset(self):
        self.ev3.light.on(Color.RED)
        wait(600)   
        #מדידת מהירות זוויתית
        print(self.gyro_sensor.speed())
        #איפוס הגירו
        self.gyro_sensor.reset_angle(0)
        #מדידת זווית
        print(self.gyro_sensor.angle())
        #מדידת זווית
        self.gyro_sensor.reset_angle(0)
        wait(400)
        self.ev3.light.off()



##### The End :) #####
if __name__ == '__main__':
    robot = Robot()
    debug = True
    #robot.pid_gyro(40)
    #print(GyroSensor.angle())
    # robot.wait_for_button("Press to turn 90 right", debug)
    # robot.turn(90, 50)
    
