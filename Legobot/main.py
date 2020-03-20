#!/usr/bin/env python2
import os
import sys
from wallaby import *
from objects import *
import constants as c
import actions as a
import sensors as s
import movement as m
import utils as u

def main():
    print "Starting main()\n"
    u.setup()
    u.calibrate_regionals()  # Calibrates tophats and motor values
    u.wait_until_round_starts()
    
    
    # Put the commands you want the robot to run here.
    
    u.shutdown()

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main()
