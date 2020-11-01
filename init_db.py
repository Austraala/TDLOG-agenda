"""
This file sets up a database for the project

   Jean-Loup Raymond
   ENPC - (c) 05/10/2020

"""

import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as file:
    connection.executescript(file.read())

cursor = connection.cursor()

cursor.execute("INSERT INTO users (first_name, last_name, gender, birth_date, email) VALUES (?, ?, ?, ?, ?)",
               ('First Name', 'Last name', 'Gender', 'Birth date', 'E-mail address')
               )

connection.commit()
connection.close()
