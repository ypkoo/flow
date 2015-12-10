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
    STUDY_BUTTON = 1
    PROG_BUTTON = 2
    REVIEW_BUTTON = 3
    BACK_BUTTON = 4
    PLAY_BUTTON = 5
    GRADE_BUTTON = 6
    LEFT_BUTTON = 7
    RIGHT_BUTTON = 8
    LIST_BUTTON = 9
    button_pushed_count = 0
    prev_button = None
    cur_button = None
    grade_on = False

    def get_pushed_button(self, state, buttons):
        back_button = buttons[-1]
        
        if back_button == '1' and (self.cur_button == self.BACK_BUTTON or self.cur_button == None):
            self.button_pushed_count = self.button_pushed_count + 1
            self.cur_button = self.BACK_BUTTON
        elif buttons.count('1') != 1:
            self.cur_button = None
            self.button_pushed_count = 0
            return False
        elif state == MENU:
            self.button_pushed_count = self.button_pushed_count + 1
            print 'pushed count', self.button_pushed_count
            if buttons[0] == '1' and (self.cur_button == self.STUDY_BUTTON or self.cur_button == None):
                print 'study button pushed'
                self.cur_button = self.STUDY_BUTTON
            elif buttons[1] == '1' and (self.cur_button == self.PROG_BUTTON or self.cur_button == None):
                self.cur_button = self.PROG_BUTTON
            elif buttons[2] == '1'and (self.cur_button == self.REVIEW_BUTTON or self.cur_button == None):
                self.cur_button = self.REVIEW_BUTTON
            else:
                self.cur_button = None
                self.button_pushed_count = 0
        elif state == LEARNING:
            pass
        elif state == SOLVING:
            if grade_on:
                self.button_pushed_count = self.button_pushed_count + 1
                if buttons[0] == '1' and (self.cur_button == GRADE_BUTTON or self.cur_button == None):
                    self.cur_button = self.GRADE_BUTTON
                else:
                    self.cur_button = None
                    self.button_pushed_count = 0
        elif state == GRADED:
            pass
        elif state == PROGRESS:
            pass
        elif state == REVIEW:
            self.button_pushed_count = self.button_pushed_count + 1
            if buttons[0] == '1' and (self.cur_button == self.LEFT_BUTTON or self.cur_button == None):
                self.cur_button = self.RIGHT_BUTTON
            elif buttons[1] == '1' and (self.cur_button == self.LIST_BUTTON or self.cur_button == None):
                self.cur_button = self.LIST_BUTTON
            elif buttons[2] == '1' and (self.cur_button == self.RIGHT_BUTTON or self.cur_button == None):
                self.cur_button = self.RIGHT_BUTTON
            else:
                self.cur_button = None
                self.button_pushed_count = 0
        else:
            self.cur_button = None
            self.button_pushed_count = 0
            return False

        if self.button_pushed_count == 3:
            self.button_pushed_count = 0
            ret = self.cur_button
            self.cur_button = None
            print 'return button:', ret
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
        network.client.sendto_sunghoi(MENU)
        network.client.sendto_saehun("1;-1;%s;-1" % title);
    else:
        network.client.sendto_sunghoi(COVER)

# virtual button recognition
def menu_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]

    button = button_handler.get_pushed_button(state.get_state(), buttons)
    if button:
        if button == button_handler.STUDY_BUTTON:
            state.set_state(BUFFER)
            network.client.sendto_saehun("1;-1;%s;1" % state.title)
        elif button == button_handler.PROG_BUTTON:
            state.set_state(PROGRESS)
            network.client.sendto_saehun("4;-1");
        elif button == button_handler.REVIEW_BUTTON:
            state.set_state(REVIEW)
            network.client.sendto_saehun("5;-1");
        elif button == button_handler.BACK_BUTTON:
            state.set_state(COVER)
            network.client.sendto_saehun("0;-1");
        network.client.sendto_sunghoi(state.get_state())
        

def buffer_handler(msg_):
    msg = msg_.split(';')

    # for mitigating instable page recognition.
    try:
        new_page = int(msg[PAGE_IDX])
    except:
        return

    page = state.get_current_page(new_page)
    #print 'page:', page

    if page != -1:
        conn = sqlite3.connect('studylamp.db')
        cursor = conn.cursor()

        page_state = db.page_state(cursor, page)
        if page_state == False:
            print 'wrong page recognized', page

        cursor.close()
        conn.close()

        if page_state == 'LEARNING':
            changed = state.set_state(LEARNING)
            if changed:
                conn = sqlite3.connect('studylamp.db')
                cursor = conn.cursor()
                chapter_num, chapter_name = db.chapter_by_page(cursor, page)

                msg_to_send = ';'.join([str(LEARNING), str(page), chapter_name, '-1'])
                network.client.sendto_saehun(msg_to_send)

                conn.commit()
                cursor.close()
                conn.close()
            learning_state_handler(msg_)
        elif page_state == 'SOLVING':
            changed = state.set_state(SOLVING)

            conn = sqlite3.connect('studylamp.db')
            cursor = conn.cursor()
            chapter_num, chapter_name = db.chapter_by_page(cursor, page)

            if chapter_num == -1:
                cursor.close()
                conn.close()
                return

            total_prob_num, solved_prob_num, correct, correct_probs, wrong_probs, graded = db.problem_state(cursor, chapter_num)
            if total_prob_num == solved_prob_num:
                button.grade_on = True
            
            conn.commit()
            cursor.close()
            conn.close()

            if changed:
                msg_to_send = ';'.join([str(SOLVING), str(page), chapter_name, str(total_prob_num), str(solved_prob_num), '-1'])
                network.client.sendto_saehun(msg_to_send)
            solving_state_handler(msg_, graded)
        elif page_state == 'GRADED':
            changed = state.set_state(GRADED)
            graded_state_handler(msg_)
        else:
            pass
            changed = False

        if changed:
            network.client.sendto_sunghoi(state.get_state())

def learning_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()

    if len(buttons) > 0:
        button = button_handler.get_pushed_button(cur_state, buttons)

        if button:
            if button == button_handler.PLAY_BUTTON:
                # need to be implemented. play video.
                pass
            elif button == button_handler.BACK_BUTTON:
                state.set_state(MENU)
                network.client.sendto_sunghoi(state.get_state())
                network.client.sendto_saehun("1;-1;%s;1" % state.title)
                return

def solving_state_handler(msg_, graded):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()
    width = int(msg[WIDTH_IDX])
    height = int(msg[HEIGHT_IDX])
    
    conn = sqlite3.connect('studylamp.db')
    cursor = conn.cursor()
    page = int(msg[PAGE_IDX])
    page = state.get_current_page(page)

    cursor.close()
    conn.close()
    
    if len(buttons) > 0:
        button = button_handler.get_pushed_button(cur_state, buttons)

        if button:
            if button == button_handler.BACK_BUTTON:
                state.set_state(MENU)
                network.client.sendto_saehun("1;-1;%s;1" % state.title)
                network.client.sendto_sunghoi(state.get_state())
                return
            if button == button_handler.GRADE_BUTTON:
                conn = sqlite3.connect('studylamp.db')
                cursor = conn.cursor()

                chapter_num, chapter_name = db.chapter_by_page(cursor, page)

                if chapter_num == -1:
                    cursor.close()
                    conn.close()
                    print 'wrong chapter number'
                    return

                db.grade_one_chapter(cursor, chapter_num)
                conn.commit()
                cursor.close()
                conn.close()

    # if check occurs
    if msg[CHECK_X_IDX] != '-1' and msg[CHECK_Y_IDX] != '-1':
        print msg[CHECK_X_IDX], msg[CHECK_Y_IDX], width, height
        # Current implementation uses only right page number. So we need post processing.
        if float(msg[CHECK_X_IDX]) < width * 0.5:
            page = page - 1

        check_x = msg[CHECK_X_IDX]
        check_y = msg[CHECK_Y_IDX]

        print '            check at',page, check_x, check_y, width, height

        conn = sqlite3.connect('studylamp.db')
        cursor = conn.cursor()

        chapter_num, chapter_name = db.chapter_by_page(cursor, page)

        if chapter_num == -1:
            cursor.close()
            conn.close()
            print 'wrong chapter number'
            return
        
        #print page, check_x, check_y, width, height
        # message format: code;page_number;total_problems;solved_problems;back

        if graded:
            prob_num = prob_num_by_check(cursor, page, check_x, check_y, width, height)
        else:
            db.check_answer(cursor, page, check_x, check_y, width, height)

            total_prob_num, solved_prob_num, correct, correct_probs, wrong_probs, graded_ = db.problem_state(cursor, chapter_num)
            if total_prob_num == solved_prob_num:
                button.grade_on = True
            msg_to_send = ';'.join([str(SOLVING), str(page), chapter_name, str(total_prob_num), str(solved_prob_num), '-1'])
            network.client.sendto_saehun(msg_to_send)

        conn.commit()
        cursor.close()
        conn.close()

def graded_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()

    if len(buttons) > 0:
        button = button_handler.get_pushed_button(cur_state, buttons)

        if button:
            if button == button_handler.BACK_BUTTON:
                state.set_state(MENU)
                network.client.sendto_sunghoi(state.get_state())

    width = int(msg[WIDTH_IDX])
    height = int(msg[HEIGHT_IDX])
    page = int(msg[PAGE_IDX])

def progress_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()

    if len(buttons) > 0:
        button = button_handler.get_pushed_button(cur_state, buttons)

        if button:
            if button == button_handler.PLAY_BUTTON:
                # need to be implemented. play video.
                pass
            elif button == button_handler.BACK_BUTTON:
                state.set_state(MENU)
                network.client.sendto_sunghoi(state.get_state())
                network.client.sendto_saehun("1;-1;%s;1" % state.title)
                return

def review_state_handler(msg_):
    msg = msg_.split(';')
    buttons = msg[BUTTON_IDX]
    cur_state = state.get_state()

    if len(buttons) > 0:
        button = button_handler.get_pushed_button(cur_state, buttons)

        if button:
            if button == button_handler.PLAY_BUTTON:
                # need to be implemented. play video.
                pass
            elif button == button_handler.BACK_BUTTON:
                state.set_state(MENU)
                network.client.sendto_sunghoi(state.get_state())
                network.client.sendto_saehun("1;-1;%s;1" % state.title)
                return
            elif button == button_handler.LEFT_BUTTON:
                pass
            elif button == button_handler.RIGHT_BUTTON:
                pass
            elif button == button_handler.LIST_BUTTON:
                pass
            else:
                pass






            
