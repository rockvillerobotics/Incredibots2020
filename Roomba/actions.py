from wallaby import *
from decorators import *
import constants as c
import sensors as s
import movement as m
import gyro as g
import utils as u

@print_function_name
def sample_command():
    m.drive(1000)
