"""
This file defines the process through which we assign a starting date to each task.

    Benjamin ROULIN
    ENPC (c)
"""

# Imports
import task

"""
    PART A - NAIVE OPTIMIZATION
    How it works :
    I.
    - Get today's date : the algorithm will only put tasks for the next day, or the day after that. It won't
        change anything today.
    II.
    - Get the constraints from a list of Fixed_Task, as a list of :
        Week, Day, Starting Time, Ending Time
    III.
    - Merge the constraints if they are the same day and week and there's an overlap in their times.
    - Order them : week, day, starting times (they are already merge if need be)
    IV.
    - Order the Mobile_Tasks in the right way
    V.
    - Take the first one : 
        - Get to the next day and check if there's time.
        - If there is, put the Mobile_Task there :
            - Add a new constraint.
            - Add a starting time and ending time to the Mobile_Task.
            - Pop it out.
        - Get to the next one.
    VII. SET-UP THE BIG FUNCTION THAT DOES IT
"""

#   I.


def get_date_as_coordinates():
    """
    This function gets today's date, and finds the relevant tuple [day, week]
    """
    #   Need to talk about how it works.

#  II.


def get_constraints(list_tasks_to_implement):
    """
    This function gets a list of tasks.
    It deletes the Fixed Ones while remembering the resulting constraints.
    It outputs a list of constraints [week, day, starting_time, ending_time].
    """
    list_constraints = []
    for constraint in list_tasks_to_implement:
        if type(constraint).__name__ == FixedTask:
            list_constraints.append([constraint.week, constraint.day, constraint.starting_time, constraint.ending_time])
            list_tasks_to_implement.remove(constraint)
    return list_constraints


#   III.
def test_simultaneity(constraint_one, constraint_two):
    """
    This function returns True if both constraints share a time slot.
    It returns False otherwise.
    """

    if constraint_one[0] == constraint_two[0] and constraint_one[1] == constraint_two[1]:
        sta_one = constraint_one[2]
        end_one = constraint_one[3]
        sta_two = constraint_two[2]
        end_two = constraint_two[3]

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
    """
    week = constraint_one[0]
    day = constraint_one[1]
    list_constraints.remove(constraint_one)
    list_constraints.remove(constraint_two)
    list_constraints.append([week, day, min(constraint_one[2], constraint_two[2]),
                             max(constraint_one[3], constraint_two[3])])
    return list_constraints


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


def compare_time_constraints(constraint_one, constraint_two):
    """
    We use this function for the sort_time_constraints function
    It return -1 if constraint_one is before constraint_two, +1 if constraint_one is after constraint_two.
    """
    if constraint_one[0] < constraint_two[0]:
        return -1
    elif constraint_one[1] < constraint_two[1]:
        return -1
    elif constraint_one[2] < constraint_two[2]:
        return -1
    return 1


def sort_time_constraints(list_constraints):
    """
    This function is used to order the list of constraints in ascending week number, day number and
    """
    return sorted(list_constraints, key=compare_time_constraints)

#   IV.


def compare_mobile_tasks(mobile_task1, mobile_task2):
    """
    We use this function for the sort_mobile_tasks function
    It returns -1 if the deadline of the first task is before the deadline of the second one
        and +1 otherwise.
    """
    compare_time_constraints(mobile_task1.deadline, mobile_task2.deadline)


def sort_mobile_tasks(list_tasks_to_implement):
    """
    This function is used to order the list of tasks from the closest deadline to the farthest.
    """
    return sorted(list_tasks_to_implement, key=compare_mobile_tasks)

#   V.


def find_time_today(list_constraints, mobile_task, day, week):
    """
    This function looks for an appropriate timeslot in the corresponding day.
    If it finds the time, it implements it and returns True (it found a solution)
        It modifies mobile_task and adds a new constraint.
    If it doesn't, it returns False. You'll have to try next day.
    """
    duration = mobile_task.duration
    constraints_today = []
    for constraint in list_constraints:
        if constraint[0] == week and constraint[1] == day:
            constraints_today.append(constraint)
    sort_time_constraints(constraints_today)
    for i in range(len(constraints_today)-1):
        start_next_task = list_constraints[i+1][2]
        end_previous_task = list_constraints[i][3]
        if start_next_task - end_previous_task >= duration:
            #   Set the starting date of the mobile_task.
            mobile_task.starting_time = end_previous_task
            #   Add a new relevant constraint.
            list_constraints.append([week, day, end_previous_task, end_previous_task+duration])
            return True
    return False

#   VII - Big Function that does everything


def optimize(list_tasks, current_week, current_day):
    """
    This function puts the mobile_tasks where it can, and gives them a starting date.
    It returns nothing.
        It updates the mobile tasks and the list of constraints.
    """
    list_constraints = sort_time_constraints(smooth_time_constraints(get_constraints(list_tasks)))
    list_tasks = sort_mobile_tasks(list_tasks)
    for mobile_task in list_tasks:
        day = current_day
        week = current_week
        while not(find_time_today(list_constraints, mobile_task, day, week)):
            if day == 6:
                day = 0
                week += 1
            else:
                day += 1


"""
    PART B - OPTIMIZATION WITH SHUFFLE
    
    How it works :
    It takes over after the Naive Optimization.
    I. Check if a couple of random tasks can be swapped.
    II. Swap two tasks and update list_constraints.
    III. Calculate score of each day :
        - Sum of the difficulties of each task of the day, squared.
        - Sum of the distance-to-deadline of each Mobile task, in days.
"""