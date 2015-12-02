__author__ = 'koo'

import network
from db_manager import *
from state import *

# states
COVER = 0
MENU = 1
LEARNING = 2
SOLVING = 3
GRADED = 4
REVIEW = 5
PROGRESS = 6
BUFFER = 7

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

class ButtonHandler(object):
    STUDY_BUTTON = 0
    PROG_BUTTON = 1
    REVIEW_BUTTON = 2
    BACK_BUTTON = 3
    PLAY_BUTTON = 4
    button_pushed_count = 0
    prev_button = None
    cur_button = None

    def get_pushed_button(self, state, buttons):
        back_button = buttons[-1]

        if back_button == '1' and (self.prev_button == self.BACK_BUTTON or self.prev_button == None):
            self.button_pushed_count = self.button_pushed_count + 1
            self.cur_button = self.BACK_BUTTON
        elif buttons.count('1') != 1:
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
            else:
                self.button_pushed_count = 0
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

def msg_dispatcher(msg):
    cur_state = state.get_state()
    msg_state = int(msg.split(';')[STATE_IDX])

    if cur_state != msg_state:
        network.client.sendto_sunghoi(cur_state)
        return

    if cur_state == COVER:
        start_state_handler(msg)
    elif cur_state == MENU:
        menu_state_handler(msg)
    elif cur_state == LEARNING:
        buffer_handler(msg)
    elif cur_state == SOLVING:
        buffer_handler(msg)
    elif cur_state == GRADED:
        buffer_handler(msg)
    elif cur_state == PROGRESS:
        progress_state_handler(msg)
    elif cur_state == REVIEW:
        review_state_handler(msg)
    elif cur_state == BUFFER:
        buffer_handler(msg)

def start_state_handler(msg_):
    msg = msg_.split(';')
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
        state.set_state(MENU)
    else:
        network.client.sendto_sunghoi(COVER)

# virtual button recognition
def menu_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]

    button = button_handler.get_pushed_button(state, buttons)
    if button:
        if button == button_handler.STUDY_BUTTON:
            state.set_state(BUFFER)
        elif button == button_handler.PROG_BUTTON:
            state.set_state(PROGRESS)
        elif button == button_handler.REVIEW_BUTTON:
            state.set_state(REVIEW)
        elif button == button_handler.BACK_BUTTON:
            state.set_state(COVER)
        network.client.sendto_sunghoi(state.state)
        network.client.sendto_saehun("1;-1;%s;1" % state.title)

def buffer_handler(msg_):
    msg = msg_.split(';')

    # for mitigating instable page recognition.
    try:
        new_page = int(msg[PAGE_IDX])
    except:
        return

    page = state.get_current_page(new_page)

    if page != -1:
        conn = sqlite3.connect('studylamp.db')
        cursor = conn.cursor()

        page_state = db.page_state(cursor, page)

        cursor.close()
        conn.close()

        if page_state == 'LEARNING':
            changed = state.set_state(LEARNING)
            learning_state_handler(msg_)
        elif page_state == 'SOLVING':
            changed = state.set_state(SOLVING)
            solving_state_handler(msg_)
        elif page_state == 'GRADED':
            changed = state.set_state(GRADED)
            graded_state_handler(msg_)

        if changed:
            network.client.sendto_sunghoi(state.get_state())

def learning_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()
    button = button_handler.get_pushed_button(cur_state, buttons)

    if button:
        if button == button_handler.PLAY_BUTTON:
            # need to be implemented. play video.
            pass
        elif button == button_handler.BACK_BUTTON:
            state.set_state(MENU)
            network.client.sendto_sunghoi(state.state)
        network.client.sendto_saehun("1;-1;%s;1" % state.title)

def solving_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()
    button = button_handler.get_pushed_button(cur_state, buttons)

    if button:
        if button == button_handler.BACK_BUTTON:
            state.set_state(MENU)
            network.client.sendto_sunghoi(state.state)

    width = int(msg[WIDTH_IDX])
    height = int(msg[HEIGHT_IDX])
    page = int(msg[PAGE_IDX])

    # if check occurs
    if msg[CHECK_X_IDX] != '-1' and msg[CHECK_Y_IDX] != '-1':
        # Current implementation uses only right page number. So we need post processing.
        if float(msg[CHECK_X_IDX]) < width * 0.5:
            check_x = msg[CHECK_X_IDX]
            check_y = msg[CHECK_Y_IDX]
            page = page - 1
        else:
            check_x = float(msg[CHECK_X_IDX]) - width * 0.5
            check_y = msg[CHECK_Y_IDX]

        print 'check at', check_x, ',', check_y

        conn = sqlite3.connect('studylamp.db')
        cursor = conn.cursor()

        chapter_num, chapter_name = db.chapter_by_page(cursor, page)

        # message format: code;page_number;total_problems;solved_problems;back
        db.check_answer(cursor, page, check_x, check_y, width, height)

        total_prob_num, solved_prob_num = db.problem_state(cursor, chapter_num)

        msg_to_send = ';'.join([SOLVING, str(page), chapter_name, str(total_prob_num), str(solved_prob_num), '-1'])
        network.client.sendto_saehun(msg_to_send)

        conn.commit()
        cursor.close()
        conn.close()

def graded_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()
    button = button_handler.get_pushed_button(cur_state, buttons)

    if button:
        if button == button_handler.BACK_BUTTON:
            state.set_state(MENU)
            network.client.sendto_sunghoi(state.state)

    width = int(msg[WIDTH_IDX])
    height = int(msg[HEIGHT_IDX])
    page = int(msg[PAGE_IDX])

def progress_state_handler(msg_):
    pass

def review_state_handler(msg_):
    pass
