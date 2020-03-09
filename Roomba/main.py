#!/usr/bin/env python2
import os
import sys
from wallaby import *
import constants as c
import actions as a
import movement as m
import sensors as s
import gyro as g
import utils as u

def main():
    print "Starting main()\n"
    u.setup()
    # u.calibrate()  # You only need to include this command if you want the cliffs to sense better at the cost of speed.
    # get the orange ball
    g.turn_left_gyro()
    g.forwards_gyro_until_black_lfcliff()
    g.forwards_gyro_until_white_lfcliff()
    g.forwards_gyro_until_black_lfcliff()
    g.forwards_gyro_until_white_lfcliff()
    g.forwards_gyro_until_black_lcliff()
    g.forwards_gyro_until_white_lcliff()
    s.turn_left_until_rfcliff_senses_black()
    s.turn_left_until_rfcliff_senses_white()
    s.turn_left_until_rcliff_senses_black()
        
    # line up to the corner
    s.turn_right_until_rfcliff_senses_black()
    s.turn_right_until_rcliff_senses_white()
    s.turn_right_until_rcliff_senses_black()
    s.turn_left_until_lcliff_senses_white()
    s.turn_right_until_lcliff_senses_black()
    s.turn_right_until_lcliff_senses_white()
    g.forwards_gyro_until_black_rfcliff()
    g.forwards_gyro_until_white_rfcliff()
    g.forwards_gyro_until_black_lcliff()
    g.turn_left_gyro()
    g.turn_left_gyro()
    g.turn_left_gyro()
    g.forwards_gyro_until_white_rfcliff()
    g.forwards_gyro_until_black_rfcliff()
    g.forwards_gyro_until_bump()
    g.turn_left_gyro()
    g.turn_left_gyro()
    g.turn_left_gyro()
    g.turn_left_gyro()

        
        
        
        
        
        
if __name__== "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(),"w",0)
    main();