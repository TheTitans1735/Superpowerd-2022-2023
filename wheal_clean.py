#!/usr/bin/env pybricks-micropython
from robot import *
import time
from functools import wraps

ilan = Robot()


def wheal_clean():
    ilan.run_straight(5000)


wheal_clean()
