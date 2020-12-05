"""
This file sets up a database for the project

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable=E0401

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, with_polymorphic

from entities.user import User
from entities.task import Base, Task, FixedTask, MobileTask
from algorithm.crypto import encrypt
# from entities.schedule import Schedule, Week, Day

# pylint: disable=E1101


# Sets things up for sqlalchemy
engine = create_engine("sqlite+pysqlite:////database.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

fixed_plus_mobile = with_polymorphic(Task, '*')
query = session.query(fixed_plus_mobile)

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
                  .first()[0], 'Math', 80, 10)
task_dummy_2 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                    .first()[0], 'English', 60, 4)
user_dummy.tasks = [task_dummy, task_dummy_2]
# Add it to the database
session.add(task_dummy, task_dummy_2)
session.commit()


# fixed and mobile task dummies
task_dummy_3 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                    .first()[0], 'Mechanics', 90, 9)
fixed_task_dummy_1 = FixedTask(task_dummy_3, '16/04/2000', False)
task_dummy_4 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                    .first()[0], 'Stat. Phy.', 45, 6)
fixed_task_dummy_2 = FixedTask(task_dummy_4, '16/04/2000', True)
user_dummy.tasks += [fixed_task_dummy_1, fixed_task_dummy_2]
session.add(fixed_task_dummy_1, fixed_task_dummy_2)
session.commit()

task_dummy_5 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                    .first()[0], 'Programming', 120, 7)
mobile_task_dummy_1 = MobileTask(task_dummy_5, 'December 10th', 3)
task_dummy_6 = Task(session.query("id FROM users WHERE username = 'Archlinux'")
                    .first()[0], 'Spanish', 50, 8)
mobile_task_dummy_2 = MobileTask(task_dummy_6, 'January 13th', 1)
user_dummy.tasks += [mobile_task_dummy_1, mobile_task_dummy_2]
session.add(mobile_task_dummy_1, mobile_task_dummy_2)
session.commit()

session.close()

print(session.query(User).all())
print(session.query(Task).all())
print(session.query(FixedTask).all())
print(session.query(MobileTask).all())
