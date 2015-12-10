__author__ = 'koo'

import sqlite3
from math import hypot

class DBManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def get_book_title(self, cursor, hash_val):

        # comparing two hash value. (from pHash)
        def hamming_distance(hash1, hash2):
            x = hash1 ^ hash2
            m1 = 0x5555555555555555
            m2 = 0x3333333333333333
            h01 = 0x0101010101010101
            m4 = 0x0f0f0f0f0f0f0f0f

            x -= (x >> 1) & m1
            x = (x & m2) + ((x >> 2) & m2)
            x = (x + (x >> 4)) & m4

            return (x * h01) >> 56
            #return bin(x).count('1')

        cursor.execute('''
            SELECT hash_val, book_title
            FROM covers
            '''
        )

        results = cursor.fetchall()

        max_dist = -1
        book_title = None
        for result in results:
            dist = hamming_distance(int(hash_val, 16), int(result[0], 16))
            print bin(dist).count('1')
            if dist > max_dist:
                max_dist = dist
                book_title = result[1]

        if max_dist > 0.7:
            return book_title 
        else:
            return False

    def page_state(self, cursor, page):
        cursor.execute('SELECT type, chapter_num, level FROM page WHERE page_num=%s' % page)
        result = cursor.fetchone()
        try:
            type_ = result[0]
        except:
            #print 'wrong page recognized'
            return False
        chapter_num = result[1]
        level = result[2]

        if type_ == 'LEARNING':
            return 'LEARNING'
        elif type_ == 'EXERCISE':
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
            dist = hypot(int(check_x) - result[0], int(check_y) - result[1])
            print check_x, result[0], check_y, result[1], result[2]
            if dist < min_dist:
                min_dist = dist
                min_result = result

        if min_dist < 20:
            prob_num = min_result[2]
            ans_num = min_result[3]

            cursor.execute('''
            UPDATE user_answer
            SET user_answer=%s, solved='TRUE'
            WHERE chapter_num=%s AND level=%s AND prob_num=%s
            ''' % (ans_num, chapter_num, level, prob_num))

            print '(%s, %s) checked at chapter %s, level %s' % (prob_num, ans_num, chapter_num, level)

    def prob_num_by_check(self, cursor, page, check_x, check_y, width, height):
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
            dist = hypot(int(check_x) - result[0], int(check_y) - result[1])
            print check_x, result[0], check_y, result[1], result[2]
            if dist < min_dist:
                min_dist = dist
                min_result = result

        if min_dist < 30:
            prob_num = min_result[2]
            ans_num = min_result[3]

        
        prob_num = min_result[2]

        return prob_num
    
    def chapter_by_page(self, cursor, page):
        cursor.execute('''
        SELECT chapter_num
        FROM page
        WHERE page_num=%s
        ''' % page)

        try:
            chapter_num = cursor.fetchone()[0]
        except:
            return -1,-1

        cursor.execute('''
        SELECT chapter_name
        FROM chapter
        WHERE chapter_num=%s
        ''' % chapter_num)


        
        
        try:
            chapter_name = cursor.fetchone()[0]
        except:
            return -1, -1
        
        
        return chapter_num, chapter_name

    def problem_state(self, cursor, chapter_num):
        cursor.execute('''
        SELECT solved, correct, level, prob_num
        FROM user_answer
        WHERE chapter_num=%s
        ''' % chapter_num)

        results = cursor.fetchall()
        total = 0
        solved = 0
        correct = 0
        correct_probs = []
        wrong_probs = []

        for result in results:
            total = total + 1
            if result[0] == 'TRUE':
                solved = solved + 1
            if result[1] == 'TRUE':
                correct = correct + 1
                correct_probs.append([result[2], result[3]])
            else:
                wrong_probs.append([result[2], result[3]])

        cursor.execute('''
        SELECT graded
        FROM chapter
        WHERE chapter_num=%s
        ''' % chapter_num)

        result = cursor.fetchone()

        if result[0] == 'TRUE':
            graded = True
        else:
            graded = False

        return total, solved, correct, correct_probs, wrong_probs, graded

    def grade_one_chapter(self, cursor, chapter_num):
        correct_num = 0
        wrong_num = 0
        correct_probs = []
        wrong_probs = []

        cursor.execute('''
        SELECT level, prob_num, user_answer, solved
        FROM user_answer
        WHERE chapter_num=%s
        ''' % chapter_num)

        user_answers = cursor.fetchall()

        for user_answer in user_answers:
            level = user_answer[0]
            prob_num = user_answer[1]
            answer = user_answer[2]
            solved = user_answer[3]

            if solved == 'TRUE':
                cursor.execute('''
                SELECT ans_num
                FROM answer
                WHERE chapter_num=%s AND level=%s AND prob_num=%s
                ''' % (chapter_num, level, prob_num))

                correct_answer = cursor.fetchone()[0]

                if answer == correct_answer:
                    correct_num = correct_num + 1
                    correct_probs.append([level, prob_num])

                    cursor.execute('''
                    UPDATE user_answer
                    SET graded=%s AND correct=%s
                    WHERE chapter_num=%s AND level=%s AND prob_num=%s
                    ''' % ('TRUE', 'TRUE', chapter_num, level, prob_num))

                else:
                    wrong_num = wrong_num + 1
                    wrong_probs.append([level, prob_num])

                    cursor.execute('''
                    UPDATE user_answer
                    SET graded=%s AND correct=%s
                    WHERE chapter_num=%s AND level=%s AND prob_num=%s
                    ''' % ('TRUE', 'FALSE', chapter_num, level, prob_num))

        cursor.execute('''
        UPDATE chapter
        SET graded=%s
        WHERE chapter_num=%s
        ''' % ('TRUE', chapter_num))


db = DBManager('studylamp.db')

if __name__ == "__main__":
    conn = sqlite3.connect('cover.db')
    cursor = conn.cursor()

    hash_val = '15730864853536670846'
    hash_vals = ['15730864853536670846',
                 '99990864859999670846',
                 '15738888853536888846',
                 '10000864000036670846',
                 '00000000000000000000',
                 '99999999999999999999',
                 '15730794484792497278',
                 '15730794484782497279']

    for hash_val in hash_vals:
        print 'as'
        title = db.get_book_title(cursor, hash_val)

    # title = db.get_book_title(cursor, hash_val)
    #
    # if title:
    #     print title
