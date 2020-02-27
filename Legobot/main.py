#!/usr/bin/env python2
import os
import sys
import constants as c
import actions as a
import sensors as s
import movement as m
import gyro as g
import webcam as w
import utils as u

from ctypes import cdll
kipr = cdll.LoadLibrary("./libwallaby.so")  # Access wallaby commands through kipr object


def main():
    print "Starting main()\n"
    u.setup()
    u.calibrate()
    a.get_ambulance()
    a.get_blocks()
    a.deliver_ambulance_and_blocks()
    #a.get_firefighters()
    #a.deliver_firefighters()
    u.shutdown()

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
