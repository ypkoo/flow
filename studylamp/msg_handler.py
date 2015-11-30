__author__ = 'koo'

import network
from db_manager import *
from state import *

# msg code
START = 0
MENU = 1
LEARNING = 2
SOLVING = 3
GRADED = 4
PROGRESS = 5
REVIEW = 6

# msg indexes in study state
STATE_IDX = 0
WIDTH_IDX = 1
HEIGHT_IDX = 2
FINGER_X_IDX = 3
FINGER_Y_IDX = 4
CHECK_X_IDX = 5
CHECK_Y_IDX = 6
PAGE_IDX = 7
BUTTON_IDX = 8



def msg_dispatcher(msg):
    state_ = state.state

    # book cover recognition
    if state_ == 0:
        start_state_handler(msg)
    # menu
    elif state_ == 1:
        menu_state_handler(msg)
    # study
    elif state_ == 2:
        study_state_handler(msg)
    # progress
    elif state_ == 5:
        pass
    # review
    elif state_ == 6:
        pass

def start_state_handler(msg_):
    msg = msg_.split(';')[1]

    if msg[0] != 0:
        network.client.sendto_sunghoi('0')
        return

    hash_val = msg[1]
    conn = sqlite3.connect('studylamp.db')
    cursor = conn.cursor()
    title = db.get_book_title(cursor, hash_val)
    cursor.close()
    conn.close()
    # title = "EBS SooNueng Math"

    if title:
        state.title = title
        print("book %s is recognized." % title)
        state.state = 2
    else:
        network.client.sendto_sunghoi('0')

class ButtonHandler(object):
    STUDY_BUTTON = 0
    PROG_BUTTON = 1
    REVIEW_BUTTON = 2
    BACK_BUTTON = 3
    button_pushed_count = 0
    prev_button = None
    cur_button = None

    def get_pushed_button(self, state, buttons):
        back_button = buttons[-1]

        if back_button == '1' and (self.prev_button == self.BACK_BUTTON or self.prev_button == None):
            self.button_pushed_count = self.button_pushed_count + 1
            self.cur_button = self.BACK_BUTTON
        elif buttons.count('1') >= 2:
            self.button_pushed_count = 0
            return False
        elif state == MENU:
            self.button_pushed_count = self.button_pushed_count + 1
            if buttons[0] == '1' and (self.prev_button == self.STUDY_BUTTON or self.prev_button == None):
                self.cur_button = self.STUDY_BUTTON
            elif buttons[1] == '1' and (self.prev_button == self.PROG_BUTTON or self.prev_button == None):
                self.cur_button = self.PROG_BUTTON
            elif buttons[2] == '1'and (self.prev_button == self.REVIEW_BUTTON or self.prev_button == None):
                self.cur_button = self.REVIEW_BUTTON
        elif state == LEARNING:
            pass
        elif state == SOLVING:
            pass
        elif state == GRADED:
            pass
        elif state == PROGRESS:
            pass
        elif state == REVIEW:
            pass
        else:
            return False

        if self.button_pushed_count == 3:
            self.button_pushed_count = 0
            ret = self.cur_button
            self.cur_button = None
            return ret
        else:
            return False

button_handler = ButtonHandler()
# virtual button recognition
def menu_state_handler(msg_):
    msg = msg_.split(';')
    state_ = state.state
    buttons = msg[BUTTON_IDX]
    if int(msg[0]) != MENU:
        network.client.sendto_sunghoi('1')
        return
    else:
        button = button_handler(state, buttons)
        if button:
            if button == button_handler.STUDY_BUTTON:
                state.state = 2
            elif button == button_handler.PROG_BUTTON:
                state.state = 3
            elif button == button_handler.REVIEW_BUTTON:
                state.state = 4
            elif button == button_handler.BACK_BUTTON:
                state.state = 0
            network.client.sendto_sunghoi(state.state)
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
            page = page - 1
            # page = 40
        else:
            # this is temporary implementation
            #check_x = msg[CHECK_X_IDX] - 0.5
            check_x = float(msg[CHECK_X_IDX]) - width * 0.5
            check_y = msg[CHECK_Y_IDX]
            # page = msg[PAGE_IDX]
            # page = 40

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

    print 'current page:', page


