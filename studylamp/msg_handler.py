__author__ = 'koo'

from network import client
import threading
from db_manager import *
from state import *

# msg code
START = '0'
MENU = '1'
LEARNING = '2'
SOLVING = '3'
GRADED = '4'
PROGRESS = '5'
MAKEUP_NOTE = '6'

# msg indexes
FINGER_X_IDX = 0
FINGER_Y_IDX = 1
CHECK_X_IDX = 2
CHECK_Y_IDX = 3
PAGE_IDX = 4

def msg_dispatcher(msg):
    state_ = state.state()

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
        state.title(title)
        print("book %s is recognized." % title)
        state.set_state(MENU)
    else:
        pass

# virtual button recognition
def menu_state_handler(msg_):
    state.set_state(STUDY)
    client.sendto_saehun("1;-1;%s;1" % state.title)


def study_state_handler(msg_):
    msg = msg_.split(";")

    # Current implementation uses only right page number. So we need post processing.
    if msg[CHECK_X_IDX] < 0.5:
        check_x = msg[CHECK_X_IDX]
        check_y = msg[CHECK_Y_IDX]
        page = msg[PAGE_IDX] - 1
    else:
        check_x = msg[CHECK_X_IDX] - 0.5
        check_y = msg[CHECK_Y_IDX]
        page = msg[PAGE_IDX]

    page_state = db.page_state(page)
    chapter_name = db.chapter_name_by_page(page)

    if page_state == 'LEARNING':
        # message format: code;page_number;chapter_name;media_name;back
        msg_to_send = ';'.join([LEARNING, page, chapter_name, '-1', '-1'])
        client.sendto_saehun(msg_to_send)
    elif page_state == 'SOLVING':
        # message format: code;page_number;total_problems;solved_problems;back
        if check_x != -1 and check_y != -1:
            db.check_answer(page, check_x, check_y)

        total_prob_num, solved_prob_num = db.problem_state(chapter_name)

        msg_to_send = ';'.join([SOLVING, page, total_prob_num, solved_prob_num, '-1'])
        client.sendto_saehun(msg_to_send)
    elif page_state == 'GRADED':
        # message format: code;page_number;total_problems;correct_answers;problem_number_to_show;back
        pass
    else:
        pass

