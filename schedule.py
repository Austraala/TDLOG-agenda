"""
This file defines the class Task for our planning system

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

# Imports
# import datetime


class Schedule:
    """
    We define a schedule by the content of its work weeks
    """

    def __init__(self, weeks):
        self.weeks = weeks


class Week:
    """
    We define a week by the work days it is made of
    """

    def __init__(self, days):
        self.days = days


class Day:
    """
    We define a day by the tasks completed in each of its five minute slots
    """

    def __init__(self, five_minutes_slots):
        self.five_minutes_slots = five_minutes_slots
