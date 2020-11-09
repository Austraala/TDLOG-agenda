"""
This file defines the class Task for our planning system

   Aaron Fargeon
   ENPC - (c) 05/10/2020

"""
# pylint: disable=E1101

# Imports
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
# from .user import Base, User
# from .task import Task, FixedTask, MobileTask


class Day:
    """
    We define a day by the tasks completed in each of its five minute slots
    """

    def __init__(self):
        self.five_minute_slots = [] * 288

    def __eq__(self, other):
        return self.five_minute_slots == other.five_minute_slots

    def __str__(self):
        print(self.five_minute_slots)

    def __repr__(self):
        # ATTENTION A CORRIGER : REPR de task a priori pas possible (taille str trop grande.
        # Risque de devenir du front, mais tests nécessaires
        for task in [self.five_minute_slots[0]] + [self.five_minute_slots[i]
                                                   for i in range(1, len(self.five_minute_slots))
                                                   if (self.five_minute_slots[i] !=
                                                       self.five_minute_slots[i - 1])]:
            task.__repr__()

    def implement_task(self, task):
        """ adds the task to the day planning """
        # ATTENTION A CORRIGER : le format de beginning_date est une date, pas un entier.
        # Prendre simplement range(task.duration // 5 ) ??
        # ATTENTION : générer l'heure de début avant le for.
        # Tests NECESSAIRES
        for i in range(task.beginning_date, task.beginning_date + task.duration):
            self.five_minute_slots[i] = task


class Week:
    """
    We define a week by the work days it is made of
    """

    def __init__(self):
        self.days = [] * 7

    def __eq__(self, other):
        return self.days == other.days

    def __str__(self):
        print(self.days)

    def __repr__(self):
        for day in self.days:
            day.__repr__()


class Schedule:
    """
    We define a schedule by the content of its work weeks
    """

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
