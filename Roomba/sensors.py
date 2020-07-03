from wombat import *
from decorators import *
import constants as c
import sensors as s
import gyro as g
import movement as m
import utils as u

#---------------------------------------------States-------------------------------------------
# Returns whether or not the statement is true.

def isRoombaBumped():
    return isLeftBumped() or isRightBumped()

def isRoombaNotBumped():
    return not(isLeftBumped() or isRightBumped())

def isBothBumped():
    return isLeftBumped() and isRightBumped()

def isBothNotBumped():
    return isLeftBumped() and isRightBumped()

def isLeftBumped():
    return get_create_lbump() == 1

def isLeftNotBumped():
    return get_create_lbump() == 0

def isRightBumped():
    return get_create_rbump() == 1

def isRightNotBumped():
    return get_create_rbump() == 0

# ---------------------- Wait Until Condition Commands --------------------------------------------
# Roomba continues whatever it's doing until an event.

def wait_until(boolean_function, time=c.SAFETY_TIME):
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        msleep(1)

# ---------------------- Basic Movement Until Boolean ----------------------------------------------
# Roomba moves until event.

@print_function_name
def forward_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    m.base_forward()
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        msleep(1)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def backwards_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    m.base_backwards()
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        msleep(1)
    if should_stop:
        m.deactivate_motors()


#-------------------------------------Basic Movement Until Cliff----------------------------------------------
# Roomba moves until either or both cliffs sense something.

@print_function_name
def forward_until_black_cliffs(should_stop=True, *, time=c.SAFETY_TIME):
#  Goes forward until both sensors have sensed black.
    m.base_forward()
    sec = seconds() + time / 1000
    while seconds() < sec and isLeftOnWhite() and isRightOnWhite():
        msleep(1)
    if isLeftOnBlack():
        while isRightOnWhite():
            msleep(1)
    else:
        while isLeftOnWhite():
            msleep(1)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def forward_until_black_fcliffs(should_stop=True, *, time=c.SAFETY_TIME):
    m.base_forward()
    sec = seconds() + time / 1000
    while seconds() < sec and isLeftFrontOnWhite() and isRightFrontOnWhite():
        msleep(1)
    if isLeftFrontOnBlack():
        while isRightFrontOnWhite():
            msleep(1)
    else:
        while isLeftFrontOnWhite():
            msleep(1)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def backwards_until_black_cliffs(should_stop=True, *, time=c.SAFETY_TIME):
#  Goes backwards until both sensors have sensed black.
    m.base_backwards()
    sec = seconds() + time / 1000
    while seconds() < sec and isLeftOnWhite() and isRightOnWhite():
        msleep(1)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def backwards_until_black_fcliffs(should_stop=True, *, time=c.SAFETY_TIME):
    m.base_backwards()
    sec = seconds() + time / 1000
    while seconds() < sec and isLeftFrontOnWhite() and isRightFrontOnWhite():
        msleep(1)
    if isLeftFrontOnBlack():
        while isRightFrontOnWhite():
            msleep(1)
    else:
        while isLeftFrontOnWhite():
            msleep(1)
    if should_stop:
        m.deactivate_motors()

#----------------------------------------------Bump-------------------------------------------

#------- Wall-Aligns ---------
# Roomba sets itself up for a wall follow on a certain side.

@print_function_name
def align_on_wall_left():
    m.base_veer_left(0.5)
    wait_until(isRoombaBumped)
    m.deactivate_motors()
    u.halve_speeds()
    m.base_turn_right()
    wait_until(isRoombaNotBumped)
    m.deactivate_motors()
    msleep(100)
    g.turn_left_gyro(4)
    msleep(100)


print_function_name
def align_on_wall_right():
    m.base_veer_right(0.5)
    wait_until(isRoombaBumped)
    m.deactivate_motors()
    u.halve_speeds()
    m.base_turn_left()
    wait_until(isRoombaNotBumped)
    m.deactivate_motors()
    msleep(100)
    g.turn_right_gyro(4)
    msleep(100)

#------- Wall-Based Bumps ---------
# "wfollow" means "wall follow." The roomba hugs the wall as it moves forward.

@print_function_name
def wfollow_left_choppy(time):
    sec = seconds() + time / 1000
    while seconds() < sec:
        if isRoombaBumped():
            if isRightBumped():
                m.backwards(100)
                m.turn_right()
            else:
                if c.FIRST_BUMP == True:
                    m.deactivate_motors()
                u.halve_speeds()
                m.base_turn_right()
                c.FIRST_BUMP = False
            msleep(50)
        else:
            m.base_veer_left(0.6)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


@print_function_name
def wfollow_left_choppy_until(boolean_function, *, time=c.SAFETY_TIME):
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        if isRoombaBumped():
            if isRightBumped():
                m.backwards(100)
                m.turn_right()
            else:
                if c.FIRST_BUMP == True:
                    m.deactivate_motors()
                u.halve_speeds()
                m.base_turn_right()
                c.FIRST_BUMP = False
            msleep(50)
        else:
            m.base_veer_left(0.6)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


@print_function_name
def wfollow_right_choppy(time):
    sec = seconds() + time / 1000
    while seconds() < sec:
        if isRoombaBumped():
            if isLeftBumped():
                m.backwards(100)
                m.turn_left()
            else:
                if c.FIRST_BUMP == True:
                    m.deactivate_motors()
                u.halve_speeds()
                m.base_turn_left()
                c.FIRST_BUMP = False
        else:
            m.base_veer_right(0.6)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()
        

@print_function_name
def wfollow_right_choppy_until(boolean_function, *, time=c.SAFETY_TIME):
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        if isRoombaBumped():
            if isLeftBumped():
                m.backwards(100)
                m.turn_left()
            else:
                if c.FIRST_BUMP == True:
                    m.deactivate_motors()
                u.halve_speeds()
                m.base_turn_left()
                c.FIRST_BUMP = False
        else:
            m.base_veer_right(0.6)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


@print_function_name
def wfollow_right_through_line_lfcliff(should_stop=True, *, time=c.SAFETY_TIME):
    wfollow_right_until(lfcliff.senses_black, should_stop=False)
    wfollow_right_until(lfcliff.senses_white, should_stop, time=time)


@print_function_name
def wfollow_right_through_line_rfcliff(should_stop=True, *, time=c.SAFETY_TIME):
    wfollow_right_until(rfcliff.senses_black, should_stop=False)
    wfollow_right_until(rfcliff.senses_white, should_stop, time=time)

@print_function_name
def wfollow_right_through_line_lcliff(should_stop=True, *, time=c.SAFETY_TIME):
    wfollow_right_until(lcliff.senses_black, should_stop=False)
    wfollow_right_until(lcliff.senses_white, should_stop, time=time)

@print_function_name
def wfollow_right_through_line_rcliff(should_stop=True, *, time=c.SAFETY_TIME):
    wfollow_right_until(rcliff.sense_black, should_stop=False)
    wfollow_right_until(rcliff.senses_white, should_stop, time=time)


# ---------- Smooth Wall Follow Commands -------------------
# Roomba hugs the wall as it moves forward. It will snake a bit faster and more cleanly.

@print_function_name
def wfollow_left_smooth(time):
    c.BASE_LM_POWER = c.FULL_LM_POWER * 1.3
    sec = seconds() + time / 1000
    while seconds() < sec:
        if isRoombaBumped():
            
            m.base_veer_right(0.9)
            c.FIRST_BUMP = False
        else:

            m.base_veer_left(0.9)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


@print_function_name
def wfollow_left_smooth_until(boolean_function, *, time=c.SAFETY_TIME):
    c.BASE_LM_POWER = c.FULL_LM_POWER * 1.3
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        if isRoombaBumped():
            m.base_veer_right(0.9)
            c.FIRST_BUMP = False
        else:

            m.base_veer_left(0.9)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


@print_function_name
def wfollow_right_smooth(time=c.SAFETY_TIME, should_stop=True):
    c.BASE_LM_POWER = c.FULL_LM_POWER * 1.3
    sec = seconds() + time / 1000
    while seconds() < sec:
        if isRoombaBumped():
            m.base_veer_left(0.9)
            c.FIRST_BUMP = False
        else:

            m.base_veer_right(0.9)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        u.change_speeds_by()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


@print_function_name
def wfollow_right_smooth_until(boolean_function, time=c.SAFETY_TIME):
    c.BASE_LM_POWER = c.FULL_LM_POWER * 1.3
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        if isRoombaBumped():
            m.base_veer_left(0.9)
            c.FIRST_BUMP = False
        else:

            m.base_veer_right(0.9)
            c.FIRST_BUMP = True
        u.normalize_speeds()
        u.change_speeds_by()
        msleep(c.LFOLLOW_REFRESH_RATE)
    u.normalize_speeds()
    if should_stop:
        m.deactivate_motors()


# -------------------------------Single Motor Align Commands ------------------------
# Pivot around a motor until an event.

@print_function_name_with_arrows
def left_forward_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    # Left motor goes forward until right cliff senses black
    m.av(c.LEFT_MOTOR, c.BASE_LM_POWER)
    wait_until(boolean_function, time=time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def right_forward_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    # Right motor goes forward until right cliff senses black
    m.av(c.RIGHT_MOTOR, c.BASE_RM_POWER)
    wait_until(boolean_function, time=time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def left_backwards_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    # Left motor goes backwards until left cliff senses black
    m.av(c.LEFT_MOTOR, -1 * c.BASE_LM_POWER)
    wait_until(boolean_function, time=time)
    if should_stop:
        m.deactivate_motors()


@print_function_name_with_arrows
def right_backwards_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    # Right motor goes back until right cliff senses black
    m.av(c.RIGHT_MOTOR, -1 * c.BASE_RM_POWER)
    wait_until(boolean_function, time=time)
    if should_stop:
        m.deactivate_motors()
    
#----------------------------------Turning Align Functions--------------
# Turn until an event.

@print_function_name
def turn_left_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    m.base_turn_left()
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        msleep(1)
    if should_stop:
        m.deactivate_motors()


@print_function_name
def turn_right_until(boolean_function, should_stop=True, *, time=c.SAFETY_TIME):
    m.base_turn_right()
    sec = seconds() + time / 1000
    while seconds() < sec and not(boolean_function()):
        msleep(1)
    if should_stop:
        m.deactivate_motors()

#----------------------------------------------Align Functions-------------------------------------------

@print_function_name_only_at_beginning
def align_close_fcliffs():
    u.halve_speeds()
    right_backwards_until(rfcliff.senses_white)
    left_backwards_until(lfcliff.senses_white)
    right_forward_until(rfcliff.senses_black)
    left_forward_until(lfcliff.senses_black)
    right_backwards_until(rfcliff.senses_white)
    left_backwards_until(lfcliff.senses_white)
    u.normalize_speeds()


@print_function_name_only_at_beginning
def align_far_fcliffs():
    u.halve_speeds()
    left_forward_until(lfcliff.senses_white)
    right_orward_until(rfcliff.senses_white)
    left_backwards_until(lfcliff.senses_black)
    right_backwards_until(rfcliff.senses_black)
    u.normalize_speeds()


@print_function_name_only_at_beginning
def align_close_cliffs():
    u.halve_speeds()
    left_backwards_until(lcliff.senses_white)
    right_backwards_until(rcliff.senses_white)
    left_forward_until(lcliff.senses_black)
    right_forward_until(rcliff.senses_black)
    u.normalize_speeds()


@print_function_name_only_at_beginning
def align_far_cliffs():
    u.halve_speeds()
    left_forward_untile(lcliff.senses_white)
    right_forward_until(rcliff.senses_white)
    left_backwards_until(lcliff.senses_black)
    right_backwards_until(rcliff.senses_black)
    u.normalize_speeds()

#-------------------------------------------New Stuff ---------------------------------------
# TODO organize these commands into their actual places
