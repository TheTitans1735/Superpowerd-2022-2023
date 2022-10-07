#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, ColorSensor,GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media import ev3dev

from pybricks.tools import DataLog, StopWatch, wait

# Create a data log file in the project folder on the EV3 Brick.
# * By default, the file name contains the current date and time, for example:
#   log_2020_02_13_10_07_44_431260.csv
# * You can optionally specify the titles of your data columns. For example,
#   if you want to record the motor angles at a given time, you could do:

ev3 = EV3Brick()
        # CONFIGURATION ILAN
left_motor = Motor(Port.B, Direction.CLOCKWISE)
right_motor = Motor(Port.C, Direction.CLOCKWISE)
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=146)
robot.settings(straight_speed=200, straight_acceleration=100, turn_rate=100)
color_sensor_left = ColorSensor(Port.S1)
color_sensor_right = ColorSensor(Port.S2)
gyro_sensor= GyroSensor(Port.S3)
arm_motor = Motor(Port.A)
################################PID FOLLOW LINE#######################################
def pid_follow_line(line_sensor, distance, speed, Kp, white_is_right, stop_codition=None):
    robot.reset() 
    # Calculate the light threshold. Choose values based on your measurements.
    #6,71
    BLACK = 6
    WHITE = 71
    threshold = (BLACK + WHITE) / 2
    robot.reset()
    #logger = DataLog('error', 'integral','derivative','turn_rate')
    # Set the drive speed at 100 millimeters per second.
    DRIVE_SPEED = speed

    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drivebase to 1.2 degrees per second.

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.
    PROPORTIONAL_GAIN = Kp
    DERIVATIVE_GAIN = 0.06
    INTEGRAL_GAIN = 0.007
    integral = 0
    derivative =0
    last_error = 0

    
    # Start following the line endlessly.
    #while True:
    while (robot.distance() < distance*10):
        # Calculate the deviation from the threshold.
        error = line_sensor.reflection() - threshold
        integral = integral + error
        derivative = error - last_error
        
        # Calculate the turn rate.
        turn_rate = PROPORTIONAL_GAIN * error + DERIVATIVE_GAIN * derivative + INTEGRAL_GAIN * integral
        if white_is_right:
            turn_rate = turn_rate * -1
        # Set the drive base speed and turn rate.
        robot.drive(DRIVE_SPEED, turn_rate)
        #print("distance = " + robot.distance() + " reflection = " + line_sensor.reflection() + " error = " + error + 
        #    " integral = " + integral + " derivative = " + derivative + " turn_rate = " + turn_rate)
        last_error = error
        # You can wait for a short time or do other things in this loop.
        if stop_codition:
            if stop_codition():
                break
        wait(10)
    #print(logger)    
    robot.stop()

################################PID FOLLOW LINE#######################################
def pid_follow_line2(line_sensor, distance, speed, Kp, white_is_right, stop_codition=None, count_stop_conditions = 6):
    robot.reset() 
    # Calculate the light threshold. Choose values based on your measurements.
    #6,71
    BLACK = 6
    WHITE = 71
    threshold = (BLACK + WHITE) / 2
    robot.reset()
    #logger = DataLog('error', 'integral','derivative','turn_rate')
    # Set the drive speed at 100 millimeters per second.
    DRIVE_SPEED = speed

    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drivebase to 1.2 degrees per second.

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.
    PROPORTIONAL_GAIN = Kp
    DERIVATIVE_GAIN = 0.06
    INTEGRAL_GAIN = 0.007
    integral = 0
    derivative =0
    last_error = 0
    stop_condition_count=0
    
    # Start following the line endlessly.
    #while True:
    while (robot.distance() < distance*10):
        # Calculate the deviation from the threshold.
        error = line_sensor.reflection() - threshold
        integral = integral + error
        derivative = error - last_error
        
        # Calculate the turn rate.
        turn_rate = PROPORTIONAL_GAIN * error + DERIVATIVE_GAIN * derivative + INTEGRAL_GAIN * integral
        if white_is_right:
            turn_rate = turn_rate * -1
        # Set the drive base speed and turn rate.
        robot.drive(DRIVE_SPEED, turn_rate)
        #print("distance = " + robot.distance() + " reflection = " + line_sensor.reflection() + " error = " + error + 
        #    " integral = " + integral + " derivative = " + derivative + " turn_rate = " + turn_rate)
        last_error = error
        # You can wait for a short time or do other things in this loop.
        if stop_codition:
            print("max whites:" + str(count_stop_conditions) + " current: " + str(stop_condition_count))
            if stop_condition_count < count_stop_conditions:
                stop_condition_count = stop_condition_count + 1
            else:
                break
            #if stop_codition():
            #    break
        wait(10)
    #print(logger)    
    robot.stop()


################################PID GYRO##############################################
def pid_gyro(Td, Ts = 100, Kp = 1.3, Ki= 0.025, Kd = 3):
        robot.reset() 
        gyro_sensor.reset_angle(0)
        #Td = 1000 # target distance
        #Ts = 150 # target speed of robot in mm/s
        #Kp = 3 #  the Constant 'K' for the 'p' proportional controller

        integral = 0 # initialize
        #Ki = 0.025 #  the Constant 'K' for the 'i' integral term

        derivative = 0 # initialize
        lastError = 0 # initialize
        #Kd = 3 #  the Constant 'K' for the 'd' derivative term
        #print(robot.distance())
        while (robot.distance() < Td):
            error = gyro_sensor.angle() # proportional 
            print("distance: " + str(robot.distance()) + " gyro: " + str(gyro_sensor.angle()))
            if (error == 0):
                integral = 0
            else:
                integral = integral + error    
            derivative = error - lastError  
        
            correction = (Kp*(error) + Ki*(integral) + Kd*derivative) * -1
        
            robot.drive(Ts, correction)

            lastError = error  
            #print("error " + str(error) + "; integral " + str(integral) + "; correction " + str(correction)  )    
            
        robot.stop()


# robot.drive(50,0)
#  robot.straight(500)
stop_on_white = lambda : color_sensor_left.reflection() > 70
stop_on_black = lambda : color_sensor_left.reflection() < 10
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_white)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_black)
robot.straight(35)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_white)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_black)
robot.straight(35)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_white)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_black)
robot.straight(35)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_white)
pid_follow_line(color_sensor_right,70,120,1.1,True, stop_codition=stop_on_black)
robot.straight(35)


#pid_follow_line2(color_sensor_right,70,120,1.1,True, stop_on_white,6)

#robot.turn(20)
#robot.straight(80)
# wait(10000)
#robot.stop()