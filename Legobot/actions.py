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
