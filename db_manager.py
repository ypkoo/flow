__author__ = 'koo'

import sqlite3

class DBManager:
    def __init__(self):
        self.title = None

    def set_title(self, title):
        self.title = title

    def is_page_learning(self, page):
        pass

    def is_page_solving(self, page):
        return True

    def is_page_solved(self, page):
        pass

    def check_answer(self, page, check_x, check_y):
        print("check %s, %s at page %s" % (check_x, check_y, page))


db = DBManager()