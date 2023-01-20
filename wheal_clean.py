#!/usr/bin/env pybricks-micropython
from robot import *
import time
from functools import wraps

ilan = Robot()

def forwards():
    ilan.run_straight(5000)

def Backwards():
    ilan.run_straight(-5000)

def anoyying():
    ilan.check_gyro()

    anoyying()