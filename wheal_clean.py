#!/usr/bin/env pybricks-micropython
from robot import *
import time
from functools import wraps

ilan = Robot()
def pid_gyro_test():
    ilan.pid_gyro(100,200,True,3.1,0.025,3.3)

def forwards():
    ilan.run_straight(5000)

def Backwards():
    ilan.run_straight(-5000)

def anoyying():
    ilan.check_gyro()

pid_gyro_test()