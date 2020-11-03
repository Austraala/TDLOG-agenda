"""
This file defines the process through which we assign a starting date to each task.

    Benjamin ROULIN
    ENPC (c)
"""

# Imports
# import task
# import scipy


#  USEFUL FUNCTIONS

def merge_time_constraints(constraint_one, constraint_two):
    """
    This function merges two time constraints.
    For example, if there is a fixed task from 11:00 to 13:00,
    and one from 11:30 to 14:00, it will merge
    them into one single task from 11:00 to 14:00.
    """

    return [min(constraint_one[0], constraint_two[0]), max(constraint_one[1], constraint_two[1])]


def test_simultaneity(constraint_one, constraint_two):
    """
    This function returns True if both constraints share a time slot.
    It returns False otherwise.
    """

    sta_one = constraint_one[0]
    end_one = constraint_one[1]
    sta_two = constraint_two[0]
    end_two = constraint_two[1]

    return (sta_one <= sta_two and sta_one <= sta_two <= end_one) or \
           (sta_two <= sta_one and sta_two <= sta_one <= end_two) or \
           (sta_two <= sta_one and end_one <= end_two) or \
           (sta_one <= sta_two and end_one <= end_two)


def smooth_time_constraints(list_constraints):
    """
    This function is used to reduce the amount of elements
    in the list of constraints by merging them.
    """

    for constraint_one in list_constraints:
        for constraint_two in list_constraints:
            if test_simultaneity(constraint_one, constraint_two):
                merge_time_constraints(constraint_one, constraint_two)


def register_constraint(fixed_task, list_constraints):
    """
    This function gets the time constraints from FixedTask and adds it to a list of constraints.
    Every element of a list of constraint is a tuple [Starting time ; Ending Time]
    """

    list_constraints.append(fixed_task.beginning_date,
                            fixed_task.beginning_date + fixed_task.duration)


# We have a list of constraints. It is now time to optimize
# the beginning dates of the MobileTasks so that a maximum
# number of them are finished before their deadlines.
