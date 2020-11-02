"""
This file defines the class Task for our planning system

   Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

# Imports
import task


class Day:
    """
    We define a day by the tasks completed in each of its five minute slots
    """

    def __init__(self, length):
        self.five_minute_slots = []*length

    def __eq__(self, other):
        return self.five_minute_slots == other.five_minute_slots

    def __str__(self):
        print(self.five_minute_slots)

    def __repr__(self):
        # Renvoyer plus de détails : fonctions sur task
        print([self.five_minute_slots[0]] + [self.five_minute_slots[i] for i in renge(1, len(self.five_minute_slots)) if self.five_minute_slots[i] != self.five_minute_slots[i-1]])

    def implement_task(self, task):
        for i in range(task.beginning_date, task.beginning_date + task.duration):
            self.five_minute_slots[i] = task


class Week:
    """
    We define a week by the work days it is made of
    """

    def __init__(self, length):
        self.days = []*length

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
        for week in self.weeks:
            week.days[day_number].implement_task(task)
