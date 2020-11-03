"""
This file sets up a database for the project

   Jean-Loup Raymond
   ENPC - (c)

"""

import sqlite3
from crypto import encrypt

connection = sqlite3.connect('database.db')

with open('schema.sql') as file:
    connection.executescript(file.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO users (username, password, gender, email) VALUES (?, ?, ?, ?)",
               ('User name', 'Hashed Password', 'Gender', 'E-mail address')
               )

cursor.execute("INSERT INTO users (username, password, gender, email) VALUES (?, ?, ?, ?)",
               ('Jean-Loup.RAYMOND', encrypt('test_pass_word'.encode('utf-8')),
                'M', 'jean-loup.raymond@ponts.org')
               )

connection.commit()
connection.close()
