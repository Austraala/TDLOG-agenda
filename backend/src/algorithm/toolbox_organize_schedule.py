"""
In this file are functions that are needed and useful for the optimize function.

    Benjamin ROULIN
    ENPC (c)

"""

from datetime import datetime, timedelta

# Should probably adapt Constraints to take in Datetime instead of year, month, day


class Constraint:
    """ Defines the class constraint """
    def __init__(self, name, year, month, day, starting_time, duration, deadline, mobile, implemented):
        self.name = name
        #   string
        self.year = year
        #   int
        self.month = month
        #   int between 1 and 12
        self.day = day
        # int
        self.starting_time = starting_time
        #   int (bw 0 and 1440)
        self.duration = duration
        #   int (in minutes)
        self.deadline = deadline
        #   a Datetime
        self.mobile = mobile

        #   This one is a bool (False if still to be implemented, True otherwise)
        self.implemented = implemented

    def __lt__(self, other):
        if self.month < other.month or self.day < other.day:
            return True
        return self.starting_time < other.starting_time

    def __gt__(self, other):
        return not self.__lt__(other)

    def __str__(self):
        return str(self.month) + str(self.day) + str(self.starting_time) + str(self.name)


def time_to_hour_and_minute(time):
    """
    Input is an amount of minute (time in a day).
    Output is a tuple [hour, minute].
    """
    return [time // 60, time % 60]


def minute_and_hour_to_time(minute, hour):
    """
    Same as before, but the opposite.
    """
    return hour * 60 + minute


def check_simultaneity(constraint_one, constraint_two):
    """
    This function returns True if both constraints share a time slot.
    It returns False otherwise.
    """

    if constraint_one.month == constraint_two.month and constraint_one.day == constraint_two.day:
        sta_one = constraint_one.starting_time
        end_one = sta_one + constraint_one.duration
        sta_two = constraint_two.starting_time
        end_two = sta_two + constraint_two.duration

        return (sta_one <= sta_two and sta_one <= sta_two <= end_one) or \
               (sta_two <= sta_one and sta_two <= sta_one <= end_two) or \
               (sta_two <= sta_one and end_one <= end_two) or \
               (sta_one <= sta_two and end_one <= end_two)

    return False


def merge_time_constraints(list_constraints, constraint_one, constraint_two):
    """
    This function merges two time constraints after deleting them from the original list.
    For example, if there is a fixed task from 11:00 to 13:00,
    and one from 11:30 to 14:00, it will merge
    them into one single task from 11:00 to 14:00.

    Both time constraints must be demonstrably simultaneous before !!
    """

    list_constraints.remove(constraint_one)
    list_constraints.remove(constraint_two)

    ending_time1 = constraint_one.starting_time + constraint_one.duration
    ending_time2 = constraint_two.starting_time + constraint_two.duration

    new_name = constraint_one.name + " and " + constraint_two.name
    starting_time = min(constraint_one.starting_time, constraint_two.starting_time)
    duration = max(ending_time1, ending_time2) - starting_time

    new_constraint = Constraint(new_name, constraint_one.month, constraint_one.day,
                                #   Starting time
                                starting_time,
                                #   Ending time
                                duration,
                                False, False, False)

    list_constraints.append(new_constraint)

    return list_constraints


def smooth_time_constraints(list_constraints):
    """
    This function is used to reduce the amount of elements
    in the list of constraints by merging them.
    """

    for constraint_one in list_constraints:
        for constraint_two in list_constraints:
            if check_simultaneity(constraint_one, constraint_two):
                merge_time_constraints(list_constraints, constraint_one, constraint_two)
    return list_constraints


def compare_time_constraints(constraint_one, constraint_two):
    """
    We use this function for the sort_time_constraints function
    It return -1 if constraint_one is before constraint_two,
    +1 if constraint_one is after constraint_two.

    It also puts any Mobile Task after any Fixed Task.
    """
    #   Make it a bool pls - I should indeed.

    #   Check if one is a fixed one and the other one isn't :
    if constraint_one.mobile != constraint_two.mobile:
        if constraint_one.mobile:
            #   it means constraint one is fixed, whereas two isn't
            return -1

    #   Check if both are fixed :
    if not constraint_one.mobile and not constraint_two.mobile:

        if constraint_one.month < constraint_two.month or constraint_one.day < constraint_two.day:
            return -1
        return -2 * (constraint_one[2] < constraint_two[2]) + 1

    #   Check if both are mobile :
    #   A deadline is a Datetime
    if constraint_one.deadline < constraint_two.deadline \
            or constraint_one.deadline < constraint_two.deadline \
            or constraint_one.deadline < constraint_two.deadline:
        return -1
    elif constraint_one.deadline > constraint_two.deadline \
            or constraint_one.deadline > constraint_two.deadline \
            or constraint_one.deadline > constraint_two.deadline:
        return 1

    #   If you can't do it, don't switch them.
    return 0


def sort_time_constraints(list_constraints):
    """
    This function is used to order the list of constraints
     in ascending week number, day number and starting_time
    """
    return sorted(list_constraints, key=compare_time_constraints)
