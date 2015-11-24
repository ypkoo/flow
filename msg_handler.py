__author__ = 'koo'

import connection
import threading
from db_manager import *
from state import *


# msg indexes
FINGER_X_IDX = 0
FINGER_Y_IDX = 1
CHECK_X_IDX = 2
CHECK_Y_IDX = 3

def msg_dispatcher(msg):
    state_ = state.get_state()

    if state_ == START:
        start_state_handler(msg)
    elif state_ == MENU:
        menu_state_handler(msg)
    elif state_ == STUDY:
        study_state_handler(msg)
    else:
        pass

def start_state_handler(msg_):
    # temporary implementation. book cover recognizing needed.
    title = "EBS SooNueng Math"

    if title:
        state.set_book_title(title)
        db.set_title(title)
        print("book %s is recognized." % title)
        state.set_state(MENU)
    else:
        pass

# virtual button recognition
def menu_state_handler(msg_):
    state.set_state(STUDY)
    connection.comm.sendto_saehun("1;-1;%s;1" % state.title)


def study_state_handler(msg_):
    msg = msg_.split(";")
    page = "14"
    finger_x = msg[0]
    finger_y = msg[1]
    check_x = msg[2]
    check_y = msg[3]

    if db.is_page_learning(page):
        pass
    elif db.is_page_solving(page):
        if check_x != -1 and check_y != -1:
            db.check_answer(page, check_x, check_y)
        connection.comm.sendto_saehun("3;14;10;15;-1")
    elif db.is_page_solved(page):
        pass
    else:
        pass

