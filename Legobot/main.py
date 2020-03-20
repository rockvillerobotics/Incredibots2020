#!/usr/bin/env python2
import os
import sys
from wallaby import *
from objects import *
import constants as c
import actions as a
import sensors as s
import movement as m
import gyro as g
import webcam as w
import utils as u

def main():
    print "Starting main()\n"
    u.setup()
    u.calibrate_regionals()  # Calibrates tophats and motor values
    off(left_motor.port)
    off(right_motor.port)
    wait_for_light(c.LIGHT_SENSOR)
    
    
    # Put the commands you want the robot to run here.
    
    u.shutdown()

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
