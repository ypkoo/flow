__author__ = 'koo'

import random

DEFAULT_MSG = ';;;'

FINGER_X_IDX = 0
FINGER_Y_IDX = 1
CHECK_X_IDX = 2
CHECK_Y_IDX = 3

STUDY_X = 0
STUDY_Y = 0

PROG_X = 0
PROG_Y = 0

REVIEW_X = 0
REVIEW_Y = 0

CHECK1_X = 0
CHECK1_Y = 0
CHECK2_X = 0
CHECK2_Y = 0
CHECK3_X = 0
CHECK3_Y = 0


def make_msg (finger_x, finger_y, check_x, check_y):
    msg = DEFAULT_MSG.split(';')
    msg[FINGER_X_IDX] = str(finger_x)
    msg[FINGER_Y_IDX] = str(finger_y)
    msg[CHECK_X_IDX] = str(check_x)
    msg[CHECK_Y_IDX] = str(check_y)

    msg = ';'.join(msg)

    return msg

def make_random_msg():
    msg = DEFAULT_MSG.split(';')
    msg[FINGER_X_IDX] = str(random.randint(0, 1000))
    msg[FINGER_Y_IDX] = str(random.randint(0, 1000))
    msg[CHECK_X_IDX] = str(random.randint(0, 1000))
    msg[CHECK_Y_IDX] = str(random.randint(0, 1000))

    msg = ';'.join(msg)

    return msg