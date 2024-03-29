"""
This file defines the class Task for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable=E1101, E0401

# Imports
from sqlalchemy import ForeignKey, Column, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from .user import Base, User


class Task(Base):
    """
    We define a Task by its day of assignment, duration, name,
    difficulty and a variety of labels to organize the planning properly
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")
    name = Column(String)
    duration = Column(Integer)
    difficulty = Column(Integer)
    type = Column(String(50))

    __mapper_args__ = dict(polymorphic_identity='tasks', polymorphic_on=type)

    def __init__(self, user_id, name, duration, difficulty):
        """ We get the duration, name, difficulty from the user"""

        self.user_id = user_id
        self.name = name
        self.duration = duration
        self.difficulty = difficulty
        self.start = None

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

    id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    start = Column(DateTime)
    task = relationship("Task", back_populates="fixed_task")

    __mapper_args__ = dict(polymorphic_identity='fixed_tasks')

    def __init__(self, task, start):
        """
        We call the __init__ function of the class Task
        and we define the additional parameters
        """

        super().__init__(task.user_id, task.name, task.duration, task.difficulty)
        self.start = start

    def __repr__(self):
        """
        Returns
        FixedTask(name : name, duration : duration minutes,
        difficulty : difficulty/10, labels : [labels]) begins on : start
        """

        return "Fixed" + super().__repr__() + " begins on : " + str(self.start)

    def __eq__(self, other):
        """ Returns True if everything is the same """

        return super().__eq__(other) * (self.start == other.start)


Task.fixed_task = relationship("FixedTask", back_populates="task")


class MobileTask(Task):
    """
    We define a MobileTask to properly model Tasks that
    don't have a defined timestamp and can be placed
    """
    __tablename__ = 'mobile_tasks'

    id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    deadline = Column(Date)
    task = relationship("Task", back_populates="mobile_task")

    __mapper_args__ = dict(polymorphic_identity='mobile_tasks')

    def __init__(self, task, deadline):
        """
        We call the __init__ function of the class Task
        and we define the additional parameters
        """
        print("-------------------------", task, "-------------------------")
        super().__init__(task.user_id, task.name, task.duration, task.difficulty)
        self.deadline = deadline

    def __repr__(self):
        """
        Returns
        MobileTask(name : name, duration : duration minutes,
        difficulty : difficulty/10, labels : [labels]) assigned on assignment_date
        to do before deadline, in divisions times
        """

        return "Mobile" + super().__repr__() + ", to do before " + str(self.deadline)

    def __eq__(self, other):
        """ Returns True if everything besides
        assignment_date is the same """

        return super().__eq__(other) * (self.deadline == other.deadline)


Task.mobile_task = relationship("FixedTask", back_populates="task")
