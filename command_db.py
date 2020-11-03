"""
This file contains useful functions to use database

   Jean-Loup Raymond
   ENPC - (c)

"""

import sqlite3
from crypto import encrypt


def use_db(request, values=()):
    """Connects to the database and executes the SQL request"""

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute(request, values)
        result = cursor.fetchall()
    finally:
        connection.commit()
        connection.close()
    return result


def add_user(username, password, gender, email):
    """Adds an user to the database"""

    request = "INSERT INTO users (username, password, gender, email) VALUES (?, ?, ?, ?)"
    use_db(request, (username, encrypt(password.encode('utf-8')), gender, email))
