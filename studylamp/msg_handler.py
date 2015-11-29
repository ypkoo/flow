__author__ = 'koo'

import network
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

# msg indexes in study state
WIDTH_IDX = 0
HEIGHT_IDX = 1
FINGER_X_IDX = 2
FINGER_Y_IDX = 3
CHECK_X_IDX = 4
CHECK_Y_IDX = 5
PAGE_IDX = 6



def msg_dispatcher(msg):
    state_ = state.state

    if state_ == 1:
        start_state_handler(msg)
    elif state_ == 2:
        menu_state_handler(msg)
    elif state_ == 3:
        study_state_handler(msg)
    else:
        pass

def start_state_handler(msg_):
    # temporary implementation. book cover recognizing needed.
    # hash_val = msg_.split(';')[0]
    # conn = sqlite3.connect('studylamp.db')
    # cursor = conn.cursor()
    # title = db.get_book_title(cursor, hash_val)
    # cursor.close()
    # conn.close()
    title = "EBS SooNueng Math"

    if title:
        state.title = title
        print("book %s is recognized." % title)
        state.state = 2
    else:
        network.client.sendto_sunghoi('0')

button_pushed_count = 0
LOGOUT_BUTTON = 0
LEARNING_BUTTON = 1
PROGRESS_BUTTON = 2
MAKEUP_BUTTON = 3
# virtual button recognition
def menu_state_handler(msg_):
    # temporary implementations
    global button_pushed_count
     
    state.state = 3
    network.client.sendto_saehun("1;-1;%s;1" % state.title)


def study_state_handler(msg_):
    msg = msg_.split(";")
    width = int(msg[WIDTH_IDX])
    height = int(msg[HEIGHT_IDX])

    # for mitigating instable page recognition.
    try:
        new_page = int(msg[PAGE_IDX])
    except:
        return

    page = state.get_current_page(new_page)

    if page == -1:
        return

    # if check occurs
    if msg[CHECK_X_IDX] != '-1' and msg[CHECK_Y_IDX] != '-1':
        # Current implementation uses only right page number. So we need post processing.
        if float(msg[CHECK_X_IDX]) < width * 0.5:
            check_x = msg[CHECK_X_IDX]
            check_y = msg[CHECK_Y_IDX]
            # page = msg[PAGE_IDX] - 1
            page = 40
        else:
            # this is temporary implementation
            #check_x = msg[CHECK_X_IDX] - 0.5
            check_x = float(msg[CHECK_X_IDX]) - width * 0.5
            check_y = msg[CHECK_Y_IDX]
            # page = msg[PAGE_IDX]
            page = 40

        conn = sqlite3.connect('studylamp.db')
        cursor = conn.cursor()

        page_state = db.page_state(cursor, page)
        chapter_num, chapter_name = db.chapter_by_page(cursor, page)

        if page_state == 'LEARNING':
            # message format: code;page_number;chapter_name;media_name;back
            msg_to_send = ';'.join([LEARNING, page, chapter_name, '-1', '-1'])
            network.client.sendto_saehun(msg_to_send)
        elif page_state == 'SOLVING':
            # message format: code;page_number;total_problems;solved_problems;back
            if check_x != -1 and check_y != -1:
                db.check_answer(cursor, page, check_x, check_y, width, height)

            total_prob_num, solved_prob_num = db.problem_state(cursor, chapter_num)

            msg_to_send = ';'.join([SOLVING, str(page), chapter_name, str(total_prob_num), str(solved_prob_num), '-1'])
            network.client.sendto_saehun(msg_to_send)
        elif page_state == 'GRADED':
            # message format: code;page_number;total_problems;correct_answers;problem_number_to_show;back
            pass
        else:
            pass

        conn.commit()
        cursor.close()
        conn.close()


