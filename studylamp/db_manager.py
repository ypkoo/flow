__author__ = 'koo'

import sqlite3
from math import hypot

class DBManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def page_state(self, cursor, page):
        cursor.execute('SELECT type, chapter_num, level FROM page WHERE page_num=%s' % page)
        result = cursor.fetchone()
        type = result[0]
        chapter_num = result[1]
        level = result[2]

        if type == 'LEARNING':
            return 'LEARNING'
        elif type == 'EXERCISE':
            cursor.execute('''
            SELECT graded
            FROM user_answer
            WHERE chapter_num=%s AND level=%s;
            ''' % (chapter_num, level))
            if cursor.fetchone()[0] == 'TRUE':
                return 'GRADED'
            else:
                return 'SOLVING'

    def check_answer(self, cursor, page, check_x, check_y, width, height):
        # fetch chapter and level information corresponding to page
        cursor.execute('''
        SELECT chapter_num, level
        FROM page
        WHERE page_num=%s
        ''' % page)
        result = cursor.fetchone()
        chapter_num = result[0]
        level = result[1]

        # fetch answer location information corresponding to page
        cursor.execute('''
        SELECT x, y, prob_num, ans_num
        FROM ans_location
        WHERE page_num=%s
        ''' % page)
        results = cursor.fetchall()

        # find problem and answer number which has minimum distance from checked location
        min_dist = 99999
        min_result = None
        for result in results:
            dist = hypot(float(check_x) - result[0]*width, float(check_y) - result[1]*height)
            print check_x, result[0]*width, check_y, result[1]*height, result[2]
            if dist < min_dist:
                min_dist = dist
                min_result = result

        if min_dist < 100:
            prob_num = min_result[2]
            ans_num = min_result[3]

            cursor.execute('''
            UPDATE user_answer
            SET user_answer=%s, solved='TRUE'
            WHERE chapter_num=%s AND level=%s AND prob_num=%s
            ''' % (ans_num, chapter_num, level, prob_num))

            print 'answer %s checked at chapter %s, level %s, problem %s' % (ans_num, chapter_num, level, prob_num)


    def chapter_by_page(self, cursor, page):
        cursor.execute('''
        SELECT chapter_num
        FROM page
        WHERE page_num=%s
        ''' % page)

        chapter_num = cursor.fetchone()[0]

        cursor.execute('''
        SELECT chapter_name
        FROM chapter
        WHERE chapter_num=%s
        ''' % chapter_num)

        chapter_name = cursor.fetchone()[0]

        return chapter_num, chapter_name

    def problem_state(self, cursor, chapter_num):
        cursor.execute('''
        SELECT solved
        FROM user_answer
        WHERE chapter_num=%s
        ''' % chapter_num)

        results = cursor.fetchall()
        total = 0
        solved = 0

        for result in results:
            total = total + 1
            if result[0] == 'TRUE':
                solved = solved + 1

        return total, solved

db = DBManager('studylamp.db')