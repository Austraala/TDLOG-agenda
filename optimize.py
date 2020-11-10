"""
This file defines the process through which we assign a starting date to each task.

    Benjamin ROULIN
    ENPC (c)
"""

# Imports
import task
# import scipy


#  USEFUL FUNCTIONS

def merge_time_constraints(list_constraints, constraint_one, constraint_two):
    """
    This function merges two time constraints after deleting them from the original list.
    For example, if there is a fixed task from 11:00 to 13:00,
    and one from 11:30 to 14:00, it will merge
    them into one single task from 11:00 to 14:00.
    """
    list_constraints.remove(constraint_one)
    list_constraints.remove(constraint_two)
    list_constraints.append([min(constraint_one[0], constraint_two[0]), max(constraint_one[1], constraint_two[1])])
    return list_constraints


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
                merge_time_constraints(list_constraints, constraint_one, constraint_two)
    return list_constraints


def generate_constraint(considered_task, list_tasks, list_constraints):
    """
    This function gets the time constraints from FixedTask and adds it to a list of constraints.
    Every element of a list of constraint is a tuple [Starting time ; Ending Time].
    It also takes out the fixed_task from the list_tasks
    """
    list_tasks.remove(considered_task)
    list_constraints.append([considered_task.beginning_date,
                            considered_task.beginning_date + considered_task.duration])


def find_deadline(mobile_task):
    """
    Returns the deadline of a mobile_task.
    """
    return mobile_task.deadline


def order_mobile_tasks(list_tasks):
    """
    Returns a list sorted by ascending deadline.
    """
    list_tasks.sort(key=find_deadline)
    return list_tasks


def optimize_tasks(list_tasks, current_time):
    """
    Plug in a list of Mobile and Fixed tasks. What this function does is :
        - Generate an empty list_constraints.
        - Take out the Fixed Tasks from the list_tasks and generate constraints from them.
        - Put the Mobile Tasks in the order from closest deadline to furthest.
        - Plug in the Mobile Tasks next in order of upcoming deadline as soon as possible, wherever it can fit it.
        - Return a list of Mobile Tasks with updated starting times.
    """
    #   Generate the empty list_constraints.
    list_constraints = []

    #   Take out the Fixed Tasks from the list_tasks and generate constraints from them.
    for task_to_check in list_tasks :
        if isinstance(task, FixedTask):
            generate_constraint(task_to_check, list_tasks, list_constraints)

    #   Order the remaining tasks (they're all Mobile) in order with the upcoming deadline.
    list_tasks = order_mobile_tasks(list_tasks)

    #
