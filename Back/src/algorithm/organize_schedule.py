"""
This file defines the process through which we assign a starting date to each task.

    Benjamin ROULIN
    ENPC (c)

"""

# Imports



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
#           ending_time, name, task].
#       How I handle time, it's now a minute thing (1440 in a day).
#

#   0.  Must create a Constraint Class (it's goint to be easier this way).

class Constraint :

    def __init__(self):
        self.name = name
        #   string
        self.week = week
        #   int
        self.day = day
        #   int
        self.starting_time = starting_time
        #   int (bw 0 and 1440)
        self.duration = duration
        #   int (in minutes)
        self.deadline = deadline
        #   a [week, day, time] list, with time in minutes

        #   This one is a bool (False if fixed, True if Mobile)
        self.mobile = False

        #   This one is a bool (False if still to be implemented, True otherwise)
        self.implemented = False

    def __eq__(self, other):
        return self.task == other.task

    def __ne__(self, other):
        return self.task != other.task

    def __lt__(self, other):
        if self.week < other.week:
            return True
        elif self.day < other.day:
            return True
        elif self.starting_time < other.starting_time:
            return True
        else :
            return False

    def __gt__(self, other):
        return not(self.__lt__(self, other))

    def __str__(self):
        return [self.week, self.day, self.starting_time, self.name]


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

#  II.


def get_constraints(list_tasks_to_implement):
    """
    This function gets a list of tasks (elements of class tasks).
    It translates them into a list of constraints. Those constraints have a starting date if fixed, and False where
        time information should be if mobile.

    Before :
    It deleted the Fixed Ones while remembering the resulting constraints.
    It outputs a list of constraints [week, day, starting_time, ending_time].
        starting_time and ending_time are in minutes (0 to 1440).
    """
    list_constraints = []
    for constraint in list_tasks_to_implement:
        mobile = type(constraint).__name__ != FixedTask
        #   False if FixedTas, True otherwise
        new_constraint = Constraint()
        new_constraint.name = constraint.name
        new_constraint.week =False
        new_constraint.day = False,
        constraint.duration = constraint.duration
        new_constraint.mobile = mobile
        if mobile:
            new_constraint.deadline = constraint.deadline
        else :
            #   That means, if the constraint is fixed
            new_constraint.week = constraint.week
            new_constraint.day = constraint.day
            new_constraint.starting_time = constraint.starting_time
        list_constraints.append(new_constraint)
    return list_constraints


#   III.
def test_simultaneity(constraint_one, constraint_two):
    """
    This function returns True if both constraints share a time slot.
    It returns False otherwise.
    """

    if constraint_one.week == constraint_two.week and constraint_one.day == constraint_two.day:
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

    week = constraint_one.week
    day = constraint_one.day
    list_constraints.remove(constraint_one)
    list_constraints.remove(constraint_two)

    ending_time1 = constraint_one.starting_time + constraint_one.duration
    ending_time2 = constraint_two.starting_time + constraint_two.duration

    new_name = constraint_one.name + " and " + constraint_two.name

    new_constraint = Constraint()
    new_constraint.name = new_name
    new_constraint.day = constraint_one.day
    new_constraint.week = constraint_one.week
    new_constraint.starting_time = min(constraint_one.starting_time, constraint_two.starting_time)
    new_constraint.duration = max(ending_time1, ending_time2) - new_constraint.starting_time

    list_constraints.append(new_constraint)

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

    It also puts any Mobile Task after any Fixed Task.
    """
    #   Make it a Booléen plis - I should indeed.

    #   Check if one is a fixed one and the other one isn't :
    if constraint_one.mobile != constraint_two.mobile:
        if constraint_one.mobile:
            #   it means constraint one is fixed, whereas two isn't
            return -1

    #   Check if both are fixed :
    if constraint_one.mobile == False and constraint_two.mobile == False:

        if constraint_one.week < constraint_two.week:
            return -1
        elif constraint_one.dy < constraint_two.day:
            return -1
        elif constraint_one[2] < constraint_two[2]:
            return -1
        return 1

    #   Check if both are mobile :
    #   A deadline is [week, day, time]
    if constraint_one.deadline[0] < constraint_two.deadline[0]:
        return -1
    elif constraint_one.deadline[0] > constraint_two.deadline[0]:
        return 1
    elif constraint_one.deadline[1] < constraint_two.deadline[1]:
        return -1
    elif constraint_one.deadline[1] > constraint_two.deadline[1]:
        return 1
    elif constraint_one.deadline[2] < constraint_two.deadline[2]:
        return -1
    elif constraint_one.deadline[2] > constraint_two.deadline[2]:
        return 1

    #   If you can't do it, don't switch them.
    return 0


def sort_time_constraints(list_constraints):
    """
    This function is used to order the list of constraints in ascending week number, day number and starting_time
    """
    return sorted(list_constraints, key=compare_time_constraints)


#   V.


def check_timeslot(end_previous_task, start_next_task, duration):
    """
    This function returns True if there is a big enough slot for the duration of the task to fit. Otherwise, it returns
        False.
    """
    if start_next_task - end_previous_task > duration :
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
    if constraints_of_that_day[0].starting_time > 0 :
        if check_timeslot(0, constraints_of_that_day[0].starting_time, duration):

            mobile_task.week = week
            mobile_task.day = day
            mobile_task.starting_date = 0
            mobile_task.implemented = True

            return True

    #   Check if there's time anywhere
    else:
        for i in range(len(constraints_of_that_day)-1):

            end_previous_task = constraints_of_that_day[i].starting_time + \
                                constraints_of_that_day[i].duration
            start_next_task = constraints_of_that_day[i+1].starting_time
            if check_timeslot(end_previous_task, start_next_task, duration):
                #   It means there's time !

                mobile_task.week = week
                mobile_task.day = day
                mobile_task.starting_time = end_previous_task
                mobile_task.implemented = True

                return True

    #   Check if there's time after the last task
    if constraints_of_that_day[0].starting_time < 1440:
        end_previous_task = constraints_of_that_day[-1].starting_time + constraints_of_that_day[-1].duration

        if check_timeslot(end_previous_task, 1440, duration):

            mobile_task.week = week
            mobile_task.day = day
            mobile_task.starting_date = end_previous_task
            mobile_task.implemented = True

            return True

    return False

#   VI - Schedule from list of constraints and constraints from list os schedules


def get_schedule(list_constraints):
    """
    A schedule is a list of weeks, with days inside, with tasks that are a list of :
        [name, starting_time, mobile, duration, deadline]
        deadline is False if fixed, or a [week, day, time] list of mobile.
        mobile is a bool
        duration is in minutes
    """
    #   It goes up to a year after. It creates 52 weeks of 7 days.
    schedule = [[[] for i in range(6)] for i in range(51)]
    for constraint in list_constraints:
        schedule[constraint.week][constraint.day].append([constraint.name, constraint.starting_time,
                                                          constraint.mobile, constraint.duration,
                                                          constraint.deadline])
    return schedule


def get_constraints(schedule, reshuffle):
    """
    A schedule is a list of weeks with days with tasks.
    We'll go through each task, creating a constraint with them.
        A task is [name, starting_time, mobile, duration, deadline]

    reshuffle is a bool :
        False if you don't need to reshuffle, so it will give you mobile constraints with day and week, and the
            bool implemented at True.
        True if you're going to reshuffle and add more tasks, so it will give you unimplemented mobile constraints
            (no day, no week, bool implemented at False).

    """
    list_constraints = []

    for week in schedule:
        for day in week:
            for task_to_constraint in day:
                new_constraint = Constraint()
                new_constraint.duration = task_to_constraint[3]
                new_constraint.deadline = task_to_constraint[4]
                new_constraint.mobile = task_to_constraint[2]

                if task_to_constraint[2] and reshuffle:
                    #   The task is mobile and we're going to reshuffle.
                    new_constraint.implemented = False
                else :
                    new_constraint.implemented = True
                    new_constraint.day = day
                    new_constraint.week = week

                list_constraints.append(new_constraint)

    return list_constraints


#   VII - Big Function that optimizes


def organize_schedule(list_tasks, current_week, current_day):
    """
    This function puts the mobile_tasks where it can, and gives each of them a starting date.

    It gets them one at a time.

    It returns a list of constraints under the form of a schedule.
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
    for constraint in list_constraints :
        check_day = day
        check_week = week
        if constraint.mobile and not constraint.implemented:
            #   only if the constraint is mobile and not implemented
            while not find_time_today(constraint):
                #   It doesn't go into the while if it fins immediately.
                #   The function find_time_today already updates it.
                if check_day == 6:
                    check_day = 0
                    check_week += 1
                else:
                    check_day += 1

    return get_schedule(list_constraints)


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
                    list_constraints.append([week, day, task.starting_time, task.starting_time + task.duration,
                                             task.name, task])
                elif type(task).__name__ == MobileTask :
                    list_tasks.append(task)
    return [list_tasks, list_constraints]



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
