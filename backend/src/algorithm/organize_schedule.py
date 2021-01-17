"""
This file defines the process through which we assign a starting date to each task.

    Benjamin ROULIN
    ENPC (c)

"""
# pylint: disable=E0401, R0902, R0913, R1705

# Imports
# from ..entities.task import FixedTask, Task, MobileTask
from .toolbox_organize_schedule import sort_time_constraints
# Constraint, time_to_hour_and_minute, minute_and_hour_to_time, check_simultaneity, \
# merge_time_constraints, smooth_time_constraints, compare_time_constraints

from .interface_organize_schedule import get_constraints, \
    get_schedule_from_constraints
# get_constraints_from_schedule


# from entities.schedule import Schedule, Week, Day


#    PART A - NAIVE OPTIMIZATION
#    How it works :
#    I.
#    - Get today's date : the algorithm will only put tasks for the next day,
#     or the day after that. It won't change anything today.
#    II.
#    - Get the constraints from a list of Fixed_Task, as a list of :
#        Week, Day, Starting Time, Ending Time, Difficulty
#    III.
#    - Merge the constraints if they are the same day and
#     week and there's an overlap in their times.
#    - Order them : week, day, starting times, difficulty (they are already merge if need be)
#    IV.
#    - Order the Mobile_Tasks in the right way
#    V.
#    - Take the first one :
#        - Get to the next day and check if there's time.
#        - If there is, put the Mobile_Task there :
#            - Add a new constraint.
#            - Add a starting time and ending time to the Mobile_Task.
#            - Pop it out.
#        - Get to the next one.
#    VII. SET-UP THE BIG FUNCTION THAT DOES IT

#   UPDATE :
#
#   What I'm modifying :
#       Because Mobile Tasks have no date, they'll be considered to be a list object :
#       [week, day, starting_time, ending_time, name, task].
#       How I handle time, it's now a minute thing (1440 in a day).
#

#   0.  Must create a Constraint Class (it's going to be easier this way).


#   V.


def check_timeslot(end_previous_task, start_next_task, duration):
    """
    This function returns True if there is a big enough slot
    for the duration of the task to fit. Otherwise, it returns False.
    """
    if start_next_task - end_previous_task > duration:
        return True
    return False


def find_time_today(mobile_task, list_constraints, day, week):
    """
    This function looks for an appropriate timeslot in the corresponding day.
    If it finds the time, it implements it and returns True (it found a solution)
    If it doesn't, it returns False. You'll have to try next day.
    """

    constraints_of_that_day = []
    duration = mobile_task.duration

    #   Look for all the constraints corresponding to the relevant day and week
    for constraint in list_constraints:
        if not constraint.week and constraint.week == week and constraint.day == day:
            constraints_of_that_day.append(constraint)

    #   Order them
    constraints_of_that_day = sort_time_constraints(constraints_of_that_day)

    #   Check if there's time before the first task
    if constraints_of_that_day[0].starting_time > 0:
        if check_timeslot(0, constraints_of_that_day[0].starting_time, duration):
            mobile_task.week = week
            mobile_task.day = day
            mobile_task.starting_date = 0
            mobile_task.implemented = True

            return True

    #   Check if there's time anywhere
    else:
        for i in range(len(constraints_of_that_day) - 1):

            end_previous_task = constraints_of_that_day[i].starting_time + \
                                constraints_of_that_day[i].duration
            start_next_task = constraints_of_that_day[i + 1].starting_time
            if check_timeslot(end_previous_task, start_next_task, duration):
                #   It means there's time !

                mobile_task.week = week
                mobile_task.day = day
                mobile_task.starting_time = end_previous_task
                mobile_task.implemented = True

                return True

    #   Check if there's time after the last task
    if constraints_of_that_day[0].starting_time < 1440:
        end_previous_task = constraints_of_that_day[-1].starting_time + \
                            constraints_of_that_day[-1].duration

        if check_timeslot(end_previous_task, 1440, duration):
            mobile_task.week = week
            mobile_task.day = day
            mobile_task.starting_date = end_previous_task
            mobile_task.implemented = True

            return True

    return False


#   VI - Schedule from list of constraints and constraints from list os schedules


#   VII - Big Function that optimizes


def organize_schedule(list_tasks, current_week, current_day):
    """
    This function puts the mobile_tasks where it can, and gives each of them a starting date.
    It gets them one at a time.
    It returns a list of constraints under the form of a list of fixed tasks.
    """

    #   Starts the next day
    day = current_day
    week = current_week
    if day == 6:
        day = 0
        week += 1
    else:
        day += 1

    list_constraints = sort_time_constraints(get_constraints(list_tasks))
    for constraint in list_constraints:
        check_day = day
        check_week = week
        if constraint.mobile and not constraint.implemented:
            #   only if the constraint is mobile and not implemented
            while not find_time_today(constraint, list_constraints, check_week, check_day):
                #   It doesn't go into the while if it fins immediately.
                #   The function find_time_today already updates it.
                if check_day == 6:
                    check_day = 0
                    check_week += 1
                else:
                    check_day += 1

    return list_constraints


#    PART B - OPTIMIZATION WITH SHUFFLE
#
#    How it works :
#    It takes over after the Naive Optimization.
#    I. Save a mobile_task_list
#    II. Check if a couple of random tasks can be swapped.
#    III. Swap two tasks and update list_constraints.
#    IV. Calculate score of each day :
#        - Sum of the difficulties of each task of the day, squared.
#        - Sum of the distance-to-deadline of each Mobile task, in days.
#        - You sum it all up, you need to have the lowest score possible.
#    V. Compare two mobile_task_lists.


def check_possible_swap(list_constraints, mobile_task1, mobile_task2):
    """
    This function does two things, just in case :
    - It orders list_constraints in ascending order.
    - It finds the two mobile_tasks and determines their available_time_slot,
     that means it determines : "starting time of the next task -
                                starting time of the mobile task"
    - if their respective duration fit in each other's available time, slot, it returns True.
    - otherwise, it returns False.
    - watch out though, we always need a task at night to sleep (it's not carry-over proof).
    """
    #   Order the time constraints at the start
    sort_time_constraints(list_constraints)

    #   Get some variables (easier to read this way)
    day1 = mobile_task1.day
    day2 = mobile_task2.day
    week1 = mobile_task1.week
    week2 = mobile_task2.week
    starting_time1 = mobile_task1.starting_time
    starting_time2 = mobile_task2.starting
    duration_time1 = mobile_task1.duration
    duration_time2 = mobile_task2.duration

    #   Find the respective indexes
    index_1 = list_constraints.index([week1, day1, starting_time1, starting_time1 + duration_time1])
    index_2 = list_constraints.index([week2, day2, starting_time2, starting_time2 + duration_time2])

    #   Find the respective available time slots
    if index_1 != len(list_constraints):
        available_time_slot1 = list_constraints[index_1 + 1][2] - starting_time1
    else:
        available_time_slot1 = 2400 - starting_time1
    if index_2 != len(list_constraints):
        available_time_slot2 = list_constraints[index_2 + 1][2] - starting_time2
    else:
        available_time_slot2 = 2400 - starting_time2

    #   Check if it's possible to swap
    return available_time_slot1 >= duration_time2 and available_time_slot2 >= duration_time1


def execute_swap(list_constraints, mobile_task1, mobile_task2):
    """
    This function checks if it's possible to swap both of the task with check_possible_swap
    """
    if check_possible_swap(list_constraints, mobile_task1, mobile_task2):
        #   Already sorted in check_possible_swap

        day1 = mobile_task1.day
        day2 = mobile_task2.day
        week1 = mobile_task1.week
        week2 = mobile_task2.week
        starting_time1 = mobile_task1.starting_time
        starting_time2 = mobile_task2.starting
        duration_time1 = mobile_task1.duration
        duration_time2 = mobile_task2.duration

        index_1 = list_constraints.index(
            [week1, day1, starting_time1, starting_time1 + duration_time1])
        index_2 = list_constraints.index(
            [week2, day2, starting_time2, starting_time2 + duration_time2])

        #   Do the actual swap
        stock1 = mobile_task1
        stock2 = mobile_task2
        list_constraints[index_1] = stock2
        list_constraints[index_2] = stock1

        #   Modification des mobile_task
        mobile_task1.starting_time = stock2.starting_time
        mobile_task1.day = stock2.day
        mobile_task1.week = stock2.week
        mobile_task2.starting_time = stock1.starting_time
        mobile_task2.day = stock1.day
        mobile_task2.week = stock1.week

        return list_constraints
    #   This way, even if the swap doesn't happen, the result is technically the same.
    return list_constraints
