"""
This file defines the class Task for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable=E1101

# Imports
import datetime
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """ We define the class User """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    gender = Column(String(1))
    email = Column(String)
    tasks = None

    def __init__(self, username, password, gender, email):
        """ We set up an user """

        self.username = username
        self.password = password
        self.gender = gender
        self.email = email
        self.tasks = []

    def __repr__(self):
        return str(self.username)

    def __eq__(self, other):
        """
        2 Users are equal if their username is the same
        """
        return self.username == other.username


class Task(Base):
    """
    We define a Task by its day of assignment, duration, name,
    difficulty and a variety of labels to organize the planning properly
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, unique=True)
    duration = Column(Integer)
    difficulty = Column(Integer)
    user = relationship("User", back_populates="tasks")

    def __init__(self, user_id, name, duration, difficulty):
        """ We get the duration, name, difficulty and labels from the user """

        self.user_id = user_id
        self.name = name
        self.duration = duration
        self.difficulty = difficulty
        self.beginning_date = None

    def __repr__(self):
        """
        Returns
        Task(name : name, duration : duration minutes,
         difficulty : difficulty/10, labels : [labels])
        """

        return "Task(name : " + str(self.name) \
               + ", duration : " + str(self.duration) \
               + " minutes, difficulty : " + str(self.difficulty) \
               + "/10)"

    def __eq__(self, other):
        """ Returns True if everything is the same """

        return (self.name == other.name and self.duration == other.duration
                and self.difficulty == other.difficulty)


User.tasks = relationship("Task", order_by=Task.id, back_populates="user")


class FixedTask(Task):
    """
    We define a FixedTask class to model properly Tasks
    that have a defined time stamp
    """
    __tablename__ = 'fixed_tasks'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    beginning_date = Column(Integer)
    recurring = Column(Boolean)
    task = relationship("Task", back_populates="task_type_id")

    def __init__(self, task, beginning_date, recurring):
        """
        We call the __init__ function of the class Task
        and we define the additional parameters
        """

        super().__init__(task.user_id, task.name, task.duration, task.difficulty)
        self.beginning_date = beginning_date
        if recurring:
            self.assign_label("recurring")

    def __repr__(self):
        """
        Returns
        FixedTask(name : name, duration : duration minutes,
        difficulty : difficulty/10, labels : [labels]) begins on : beginning_date
        """

        return "Fixed" + super().__repr__() + " begins on : " + str(self.beginning_date)

    def __eq__(self, other):
        """ Returns True if everything is the same """

        return super().__eq__(other) * (self.beginning_date == other.beginning_date)


Task.task_type_id = relationship("FixedTask", back_populates="task")


class MobileTask(Task):
    """
    We define a MobileTask to properly model Tasks that
    don't have a defined timestamp and can be placed
    """
    __tablename__ = 'mobile_tasks'

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    deadline = Column(Integer)
    division = Column(Integer)
    task = relationship("Task", back_populates="task_type_id")

    def __init__(self, task, deadline, attached, divisions):
        """
        We call the __init__ function of the class Task
        and we define the additional parameters
        """

        super().__init__(task.user_id, task.name, task.duration, task.difficulty)
        self.assignment_date = datetime.datetime.now()
        self.deadline = deadline
        self.labels.append(attached)
        self.divisions = divisions

    def __repr__(self):
        """
        Returns
        MobileTask(name : name, duration : duration minutes,
        difficulty : difficulty/10, labels : [labels]) assigned on assignment_date
        to do before deadline, in divisions times
        """

        return "Mobile" + super().__repr__() + " assigned on " + str(self.assignment_date)[:10] \
               + ", to do before " + str(self.deadline) + ", in " + str(self.divisions) + " times"

    def __eq__(self, other):
        """ Returns True if everything besides
        assignment_date is the same """

        return (super().__eq__(other) * (self.deadline == other.deadline)
                * (self.divisions == other.divisions))


Task.task_type_id = relationship("FixedTask", back_populates="task")
