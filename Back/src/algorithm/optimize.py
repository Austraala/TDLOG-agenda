"""
This file defines the process through which we assign a starting date to each task.

    Benjamin ROULIN
    ENPC (c)

"""

# Imports
from entities.task import FixedTask, Task, MovileTask
from entites.schedule import Schedule, Week, Day


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
#       Because Mobile Tasks have no date, they'll be considered to be a list object : [week, day, starting_time,
#           ending_time, name].
#       How I handle time, it's now a minute thing (1440 in a day).
#


#   I.

def time_to_hour_and_minute(time):
    """
    Input is an amount of minute (time in a day).
    Output is a tuple [hour, minute].
    """
    return [minute // 60, minute % 60]


def minute_and_hour_to_time(minute, hour):
    """
    Same as before, but the opposite.
    """
    return hour*60 + minute


def get_date_as_coordinates():
    """
    This function gets today's date, and finds the relevant tuple [day, week]
    """
    #   How do we do it ?
    #   For now, you'll just put the day and the week in the function.

#  II.


def get_constraints(list_tasks_to_implement):
    """
    This function gets a list of tasks.
    It deletes the Fixed Ones while remembering the resulting constraints.
    It outputs a list of constraints [week, day, starting_time, ending_time].
        starting_time and ending_time are in minutes (0 to 1440).
    """
    list_constraints = []
    for constraint in list_tasks_to_implement:
        if type(constraint).__name__ == FixedTask:
            list_constraints.append([constraint.week, constraint.day,
                                     constraint.starting_time, constraint.starting_time+constraint.duration,
                                     constraint.name])
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
                             max(constraint_one[3], constraint_two[3], constraint_one[4]+ "and " + constraint_two[4])])
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
    It return -1 if constraint_one is before constraint_two,
    +1 if constraint_one is after constraint_two.
    """
    #   Make it a Booléen plis - I should indeed.
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
    return compare_time_constraints(mobile_task1.deadline, mobile_task2.deadline)


def sort_mobile_tasks(list_tasks_to_implement):
    """
    This function is used to order the list of tasks from the closest deadline to the farthest.
    """
    return sorted(list_tasks_to_implement, key=compare_mobile_tasks)

#   V.


def check_timeslot(end_previous_task, start_next_task, duration) :
    """
    This function returns True if there is a big enough slot for the duration of the task to fit. Otherwise, it returns
        False.
    """
    if start_next_task - end_previous_task > duration :
        return True
    return False


def find_time_today(list_constraints, mobile_task, day, week):
    """
    This function looks for an appropriate timeslot in the corresponding day.
    If it finds the time, it implements it and returns True (it found a solution)
        It adds the mobile task to the list_constraints.
    If it doesn't, it returns False. You'll have to try next day.
    """
    duration = mobile_task.duration
    constraints_today = []
    new_constraint = [week, day, ]

    if check_timeslot(0, list_constraints[0], duration):
        constraints_today.append(

    for constraint in list_constraints:
        #   Finds all the constraints already on that day.
        if week == constraint[0] and day == constraint[1] :
            constraints_today.append(constraint)

    sort_time_constraints(constraints_today)
    #   Sort the time constraints from the earliest to the latest.

    return False

#   VII - Big Function that optimizes


def optimize(list_tasks, current_week, current_day):
    """
    This function puts the mobile_tasks where it can, and gives them a starting date.
    It returns nothing except a list of constraints.
        It updates the mobile tasks and the list of constraints.
    """
    list_constraints = sort_time_constraints(smooth_time_constraints(get_constraints(list_tasks)))

    list_tasks = sort_mobile_tasks(list_tasks)

    for mobile_task in list_tasks:
        if current_day == 6:
            day = 0
        else:
            day = current_day+1
        week = current_week
        while not find_time_today(list_constraints, mobile_task, day, week):
            if day == 6:
                day = 0
                week += 1
            else:
                day += 1
    return list_constraints

#   VIII    Get Data from Schedule


def get_constraints_from_schedule(schedule) :
    """
    Gets the mobile-tasks back from the schedule.
    Gets the rest of the tasks as constraints from the schedule.
    Schedule is supposed to be a list of weeks. Each week is a list of day and each day is a list of tasks with
        their time (in minutes since 00:00 the preceding day, so an int that goes from 0 to 1440.
    It takes a schedule in input, and gives a list of tasks (list_tasks) with the mobile ones, and a list_constraints
        with the fixed one ; so a tuple of lists.
    """
    list_constraints = []
    list_tasks = []
    for week in range(len(schedule)):
        for day in range(len(week)):
            for task in range(len(day)):
                if type(task).__name__ == FixedTask :
                    list_constraints.append([week, day, task.starting_time, task.starting_time + task.duration])
                elif type(task).__name__ == MobileTask :
                    list_tasks.append(task)
    schedule = []
    return [list_tasks, list_constraints]


def put_



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
    index_1 = list_constraints.index([week1, day1, starting_time1, starting_time1+duration_time1])
    index_2 = list_constraints.index([week2, day2, starting_time2, starting_time2+duration_time2])

    #   Find the respective available time slots
    if index_1 != len(list_constraints):
        available_time_slot1 = list_constraints[index_1+1][2] - starting_time1
    else:
        available_time_slot1 = 2400 - starting_time1
    if index_2 != len(list_constraints):
        available_time_slot2 = list_constraints[index_2+1][2] - starting_time2
    else:
        available_time_slot2 = 2400 - starting_time2

    #   Check if it's possible to swap
    if available_time_slot1 >= duration_time2 and available_time_slot2 >= duration_time1:
        #   It is possible to swap
        return True
    else:
        #   It's not possible to swap
        return False


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

        index_1 = list_constraints.index([week1, day1, starting_time1, starting_time1 + duration_time1])
        index_2 = list_constraints.index([week2, day2, starting_time2, starting_time2 + duration_time2])

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
