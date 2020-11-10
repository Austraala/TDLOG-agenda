"""
This file sets up a database for the project

   Jean-Loup Raymond
   ENPC - (c)

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Algorithm.crypto import encrypt
from Entities.task import Base, User, Task

# pylint: disable=E1101

# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:////database.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Destroys previous database
Base.metadata.drop_all(engine)

# Creates new database
Base.metadata.create_all(engine)

# Prepares an user
user_dummy = User('Archlinux', encrypt('Bullshit'), 'M', 'mail')
session.add(user_dummy)
session.commit()

# Creates dummy
task_dummy = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                  .first()[0], 'Math', 10, 10)
user_dummy.tasks = [task_dummy]
session.add(task_dummy)
session.commit()
# Add it to the database
session.add(task_dummy)
session.commit()

session.close()

print(session.query(User).all())
print(session.query(Task).all())
