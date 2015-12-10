__author__ = 'koo'

import sqlite3
import os

DB_NAME = 'studylamp.db'

if __name__ == "__main__":
    if os.path.isfile(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # book cover db initialization
    cursor.execute(
        '''
        CREATE TABLE covers(
        hash_val TEXT PRIMARY KEY NOT NULL,
        book_title TEXT NOT NULL);
        '''
    )

    cursor.execute("INSERT INTO covers (hash_val, book_title) VALUES ('15730794484792497278', 'SooNeung Math')")

    # create tables
    cursor.execute(
        '''
        CREATE TABLE page(
        page_num INT PRIMARY KEY NOT NULL,
        chapter_num INT REFERENCES chapter(chapter_num) NOT NULL,
        type TEXT NOT NULL,
        level TEXT DEFAULT NULL);
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE ans_location(
        page_num INT REFERENCES page(page_num) NOT NULL,
        x FLOAT NOT NULL,
        y FLOAT NOT NULL,
        prob_num INT NOT NULL,
        ans_num INT NOT NULL);
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE  answer(
        chapter_num INT REFERENCES chapter(chapter_num) NOT NULL,
        level INT NOT NULL,
        prob_num INT NOT NULL,
        ans_num INT NOT NULL);
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE user_answer(
        chapter_num INT REFERENCES chapter(chapter_num) NOT NULL,
        level INT NOT NULL,
        prob_num INT NOT NULL,
        user_answer INT DEFAULT NULL,
        solved BOOL DEFAULT FALSE,
        graded BOOL DEFAULT FALSE,
        correct BOOL DEFAULT NULL);
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE chapter(
        chapter_num INT PRIMARY KEY NOT NULL,
        chapter_name TEXT NOT NULL,
        total_prob_num INT NOT NULL,
        graded BOOL DEFAULT FALSE);
        '''
    )

    # insert page table records
    cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (34, 4, 'LEARNING')")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (35, 4, 'LEARNING')")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (36, 4, 'LEARNING')")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (37, 4, 'LEARNING')")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (38, 4, 'LEARNING')")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (39, 4, 'LEARNING')")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type, level) VALUES (40, 4, 'EXERCISE', 1)")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type, level) VALUES (41, 4, 'EXERCISE', 2)")
    cursor.execute("INSERT INTO page (page_num, chapter_num, type, level) VALUES (42, 4, 'EXERCISE', 3)")

    #cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (106, 11, 'LEARNING')")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (107, 11, 'LEARNING')")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (108, 11, 'LEARNING')")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (109, 11, 'LEARNING')")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (110, 11, 'LEARNING')")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type) VALUES (111, 11, 'LEARNING')")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type, level) VALUES (112, 11, 'EXERCISE', 1)")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type, level) VALUES (113, 11, 'EXERCISE', 2)")
    #cursor.execute("INSERT INTO page (page_num, chapter_num, type, level) VALUES (114, 11, 'EXERCISE', 3)")

    # insert chapter table records
    cursor.execute("INSERT INTO chapter (chapter_num, chapter_name, total_prob_num) VALUES (4, 'Exponents', 13)")
    cursor.execute("INSERT INTO chapter (chapter_num, chapter_name, total_prob_num) VALUES (11, 'Limit of infinite sequences', 13)")

    # insert answer table records
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 1, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 2, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 3, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 4, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 5, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 1, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 2, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 3, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 4, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 5, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 1, 3, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 2, 3, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (4, 3, 3, 1)")

    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 1, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 2, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 3, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 4, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 5, 1, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 1, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 2, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 3, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 4, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 5, 2, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 1, 3, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 2, 3, 1)")
    cursor.execute("INSERT INTO answer (chapter_num, level, prob_num, ans_num) VALUES (11, 3, 3, 1)")

    # insert ans_location records
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 77, 56, 1, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 175, 63, 1, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 271, 67, 1, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 81, 127, 2, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 174, 129, 2, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 272, 131, 2, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 81, 199, 3, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 175, 195, 3, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 272, 205, 3, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 75, 271, 4, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 177, 265, 4, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 269, 271, 4, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 83, 333, 5, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 173, 337, 5, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (40, 275, 339, 5, 5)")

    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 393, 69, 1, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 503, 68, 1, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 599, 73, 1, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 397, 139, 2, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 491, 135, 2, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 595, 141, 2, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 391, 201, 3, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 490, 205, 3, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 599, 205, 3, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 395, 267, 4, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 493, 269, 4, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 593, 271, 4, 5)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 385, 343, 5, 1)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 495, 341, 5, 3)")
    cursor.execute("INSERT INTO ans_location (page_num, x, y, prob_num, ans_num) VALUES (41, 589, 347, 5, 5)")
    


    # insert user_answer records
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 1, 1)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 1, 2)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 1, 3)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 1, 4)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 1, 5)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 2, 1)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 2, 2)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 2, 3)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 2, 4)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 2, 5)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 3, 1)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 3, 2)")
    cursor.execute("INSERT INTO user_answer (chapter_num, level, prob_num) VALUES (4, 3, 3)")

    conn.commit()
    conn.close()
