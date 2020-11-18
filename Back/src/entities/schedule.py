"""
This file defines the class Task for our planning system

   Aaron Fargeon
   ENPC - (c) 05/10/2020

"""
# pylint: disable=E1101, E0401

# Imports
from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship
from .user import Base, User
from .task import FixedTask


class Schedule(Base):
    """
    We define a schedule by the content of its work weeks
    """
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="schedule")

    def __init__(self, length):
        self.weeks = [] * length

    def __eq__(self, other):
        return self.weeks == other.weeks

    def __str__(self):
        print(self.weeks)

    def __repr__(self):
        for week in self.weeks:
            week.__repr__()

    def implement_recurring_task(self, task, day_number):
        """ Adds a recurring task to the planning, every week """

        for week in self.weeks:
            week.days[day_number].implement_task(task)


User.schedule = relationship("Schedule", order_by=Schedule.id, back_populates="user")


class Week(Base):
    """
    We define a week by the work days it is made of
    """
    __tablename__ = 'weeks'

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    schedule = relationship("Schedule", back_populates="weeks")

    def __init__(self, length):
        self.days = [] * length

    def __eq__(self, other):
        return self.days == other.days

    def __str__(self):
        print(self.days)

    def __repr__(self):
        for day in self.days:
            day.__repr__()


Schedule.weeks = relationship("Week", back_populates="schedule")


class Day(Base):
    """
    We define a day by the tasks completed in each of its five minute slots
    """
    __tablename__ = 'days'

    id = Column(Integer, primary_key=True)
    week_id = Column(Integer, ForeignKey('weeks.id'))
    week = relationship("Week", back_populates="days")
    fixed_task_id = Column(Integer, ForeignKey('fixed_tasks.id'))
    fixed_task = relationship("FixedTask", back_populates="day")

    def __init__(self):
        #self.five_minute_slots = [] * 288
        self.content = []

    def __eq__(self, other):
        #return self.five_minute_slots == other.five_minute_slots
        return self.content == other.content

    def __str__(self):
        print(self.content)

    def __repr__(self):
        # ATTENTION A CORRIGER : REPR de task a priori pas possible (taille str trop grande.
        # Risque de devenir du front, mais tests n�cessaires
        # for task in [self.five_minute_slots[0]] + [self.five_minute_slots[i]
        #                                            for i in range(1, len(self.five_minute_slots))
        #                                            if (self.five_minute_slots[i] !=
        #                                                self.five_minute_slots[i - 1])]:
        #     task.__repr__()
        for task in self.content:
            task.__repr__()

    def implement_task(self, task, position):
        """ adds the task to the day planning """
        # ATTENTION A CORRIGER : le format de beginning_date est une date, pas un entier.
        # Prendre simplement range(task.duration // 5 ) ??
        # ATTENTION : g�n�rer l'heure de d�but avant le for.
        # Tests NECESSAIRES
        self.content[position] = task


Week.days = relationship("Day", back_populates="week")
FixedTask.day = relationship("Day", back_populates="fixed_task")
