from wallaby import *
from decorators import *
import constants as c
import movement as m
import actions as a
import sensors as s
from rgb import YELLOW
from rgb import RED

def initialize_camera():
    # Wait two seconds for camera to initialize
    print "Initializing Camera"
    i = 0  # Counter
    print "Starting Step 1..."
    while i < 55:
        camera_update()
        i += 1
        msleep(1)
    print "Finished Step 100\n"


def graphics():
    console_clear()
    max_length = 480
    max_height = 260
    middle_length = max_length / 2
    graphics_open(max_length, max_height)  # Creates the graphics array with the given size
    graphics_fill(255, 255, 255)  # Fills screen with white

    # Place graphics here.

    graphics_update()


@print_function_name_with_arrows
def open_graphics_window():
    if not(c.IS_GRAPHICS_OPEN):
        console_clear()
        max_length = 480
        max_height = 260
        graphics_open(max_length, max_height) # Creates the graphics array with the given size
        graphics_fill(255, 255, 255)  # Fills screen with white          
    c.IS_GRAPHICS_OPEN = True


@print_function_name_with_arrows
def close_graphics_window():
    graphics_close()
    c.IS_GRAPHICS_OPEN = False

# *rgb.COLOR_NAME

MAX_LENGTH = 480
MAX_HEIGHT = 260

LEFT_EDGE = 0
RIGHT_EDGE = MAX_LENGTH
TOP_EDGE = 0
BOTTOM_EDGE = MAX_HEIGHT

YELLOW_FIREZONE_RECT_INNER_EDGE = RIGHT_EDGE / 2
YELLOW_FIREZONE_RECT_HEIGHT = BOTTOM_EDGE
LEFT_RED_FIREZONE_RECT_LEFT_EDGE = YELLOW_FIREZONE_RECT_INNER_EDGE / 3
LEFT_RED_FIREZONE_RECT_RIGHT_EDGE = 2 * YELLOW_FIREZONE_RECT_INNER_EDGE / 3
RIGHT_RED_FIREZONE_RECT_LEFT_EDGE = YELLOW_FIREZONE_RECT_INNER_EDGE + YELLOW_FIREZONE_RECT_INNER_EDGE / 3
RIGHT_RED_FIREZONE_RECT_RIGHT_EDGE = YELLOW_FIREZONE_RECT_INNER_EDGE + 2 * YELLOW_FIREZONE_RECT_INNER_EDGE / 3
RED_FIREZONE_RECT_TOP_EDGE = YELLOW_FIREZONE_RECT_HEIGHT / 3
RED_FIREZONE_RECT_BOTTOM_EDGE = 2 * YELLOW_FIREZONE_RECT_HEIGHT / 3

def draw_burning_zone_left():
    if c.IS_GRAPHICS_OPEN:
        graphics_rectangle_fill(LEFT_EDGE, TOP_EDGE, YELLOW_FIREZONE_RECT_INNER_EDGE, BOTTOM_EDGE, *YELLOW)
        graphics_rectangle_fill(LEFT_RED_FIREZONE_RECT_LEFT_EDGE, RED_FIREZONE_RECT_TOP_EDGE, LEFT_RED_FIREZONE_RECT_RIGHT_EDGE, RED_FIREZONE_RECT_BOTTOM_EDGE, *RED)
        graphics_update()

def draw_burning_zone_right():
    if c.IS_GRAPHICS_OPEN:
        graphics_rectangle_fill(YELLOW_FIREZONE_RECT_INNER_EDGE, TOP_EDGE, RIGHT_EDGE, BOTTOM_EDGE, *YELLOW)
        graphics_rectangle_fill(RIGHT_RED_FIREZONE_RECT_LEFT_EDGE, RED_FIREZONE_RECT_TOP_EDGE, RIGHT_RED_FIREZONE_RECT_RIGHT_EDGE, RED_FIREZONE_RECT_BOTTOM_EDGE, *RED)
        graphics_update()
