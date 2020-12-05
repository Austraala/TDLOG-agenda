"""

    Benjamin Roulin
    ENPC (c)

"""

from algorithm.toolbox_organize_schedule import Constraint


def get_constraints(list_tasks_to_implement):
    """
    This function gets a list of tasks (elements of class tasks).
    It translates them into a list of constraints.
    Those constraints have a starting date if fixed, and False where
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
        new_constraint = Constraint(constraint.name, False, False, False,
                                    constraint.duration, False, constraint.mobile,
                                    False)
        new_constraint.name = constraint.name
        new_constraint.week = False
        new_constraint.day = False
        constraint.duration = constraint.duration
        new_constraint.mobile = mobile
        if mobile:
            new_constraint.deadline = constraint.deadline
        else:
            #   That means, if the constraint is fixed
            new_constraint.week = constraint.week
            new_constraint.day = constraint.day
            new_constraint.starting_time = constraint.starting_time
        list_constraints.append(new_constraint)
    return list_constraints


def get_schedule_from_constraints(list_constraints):
    """
    A schedule is a list of weeks, with days inside, with tasks that are a list of :
        [name, starting_time, mobile, duration, deadline]
        deadline is False if fixed, or a [week, day, time] list of mobile.
        mobile is a bool
        duration is in minutes
    """
    #   It goes up to a year after. It creates 52 weeks of 7 days.
    schedule = [[[] for _ in range(6)] for _ in range(51)]
    for constraint in list_constraints:
        schedule[constraint.week][constraint.day].append(
            [constraint.name, constraint.starting_time,
             constraint.mobile, constraint.duration,
             constraint.deadline])
    return schedule


def get_constraints_from_schedule(schedule, reshuffle):
    """
    A schedule is a list of weeks with days with tasks.
    We'll go through each task, creating a constraint with them.
        A task is [name, starting_time, mobile, duration, deadline]

    Reshuffle is a bool :
        False if you don't need to reshuffle, so it will give you
        mobile constraints with day and week, and the bool implemented at True.
        True if you're going to reshuffle and add more tasks,
        so it will give you unimplemented mobile constraints
        (no day, no week, bool implemented at False).

    """
    list_constraints = []

    for week in schedule:
        for day in week:
            for task_to_constraint in day:
                new_constraint = Constraint(
                    task_to_constraint[0], False, False, task_to_constraint[1],
                    task_to_constraint[3], task_to_constraint[4], task_to_constraint[2],
                    False)

                if task_to_constraint[2] and reshuffle:
                    #   The task is mobile and we're going to reshuffle.
                    new_constraint.implemented = False
                else:
                    new_constraint.implemented = True
                    new_constraint.day = day
                    new_constraint.week = week

                list_constraints.append(new_constraint)

    return list_constraints
