"""
This file sets up a database for the project

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable=E0401

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from entities.user import User
from entities.task import Base, Task, FixedTask, MobileTask
from algorithm.crypto import encrypt
# from entities.schedule import Schedule, Week, Day

# pylint: disable=E1101


# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:///database.db", echo=True)
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
# Add it to the database
session.add(task_dummy)
session.commit()


# fixed and mobile task dummies
task_dummy_2 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                  .first()[0], 'Mechanics', 15, 9)
fixed_task_dummy = FixedTask(task_dummy_2, '16/04/2000', False)
user_dummy.tasks.append(fixed_task_dummy)
session.add(fixed_task_dummy)
session.commit()

task_dummy_3 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                  .first()[0], 'Programming', 20, 8)
mobile_task_dummy = MobileTask(task_dummy_3, 'november 10th', 3)
user_dummy.tasks.append(mobile_task_dummy)


session.close()

print(session.query(User).all())
print(session.query(Task).all())
