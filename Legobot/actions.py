"""The bulk of commands should go here"""

from wallaby import *
from decorators import *
from objects import *
import constants as c
import movement as m
import sensors as s
import utils as u

@print_function_name
def sample_command():
    m.drive(1000)
    left.lfollow_until(boolean=right.senses_black, mode=INSIDE_LINE)
 

@print_function_name
def pull_swings():
    s.drive_gyro()
    # Should get 100 points, but need build to be completed first. 
