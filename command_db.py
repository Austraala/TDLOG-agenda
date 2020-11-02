"""
This file contains useful functions to use database

   Jean-Loup Raymond
   ENPC - (c)

"""

import sqlite3
import crypto


def use_db(request):
    """Connects to the database and executes the SQL request"""
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute(request)
        result = cursor.fetchall()
    except Exception:
        raise ValueError from Exception
    finally:
        connection.commit()
        connection.close()
    return result


def add_user(username, password, gender, email):
    """Adds an user to the database"""
    request = '''"INSERT INTO users (username, password, gender, email)
     VALUES (?, ?, ?, ?)", ({u},{p},{g},{e})'''. \
        format(u=username, p=crypto.encrypt(password), g=gender, e=email)
    use_db(request)
