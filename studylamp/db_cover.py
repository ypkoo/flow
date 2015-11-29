__author__ = 'koo'

import sqlite3
import os

DB_NAME = 'cover.db'

if __name__ == "__main__":
    if os.path.isfile(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE covers(
        hash_val TEXT PRIMARY KEY NOT NULL,
        book_title TEXT NOT NULL);
        '''
    )

    cursor.execute("INSERT INTO covers (hash_val, book_title) VALUES ('15730794484792497278', 'SooNeung Math')")

    conn.commit()
    conn.close()