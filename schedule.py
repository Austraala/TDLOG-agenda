"""
This file defines the class Task for our planning system

   Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

# Imports
# import task


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
        for duty in [self.five_minute_slots[0]] + [self.five_minute_slots[i] for i in range(1, len(self.five_minute_slots)) if self.five_minute_slots[i] != self.five_minute_slots[i-1]]:
            duty.__repr__()

    def implement_task(self, duty):
        for i in range(duty.beginning_date, duty.beginning_date + duty.duration):
            self.five_minute_slots[i] = duty


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

    def implement_recurring_task(self, duty, day_number):
        for week in self.weeks:
            week.days[day_number].implement_task(duty)
