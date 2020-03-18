## The bulk of commands should go here

from wallaby import *
from decorators import *
import constants as c
import movement as m
import sensors as s
import utils as u
import webcam as w
import gyro as g

@print_function_name
def sample_command():
    m.drive(1000)


@print_function_name
def pull_swings():
    g.drive_gyro(500)
    msleep(100)
    g.backwards_gyro(1000)

# Should get 100 points, but need build to be completed first. 

# Test with VSCode