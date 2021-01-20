"""
This is a pytest file. To run with pytest

   Jean-Loup Raymond
   ENPC - (c)

"""


import datetime

from ...src.entities.task import Task, FixedTask, MobileTask
# from ..algorithm.optimize import

# Defines tested variables
# Name, duration, difficulty
task_try = Task(0, 'Try', 10, 5)
# Task, start, Recurring
fixed_task_try = FixedTask(task_try, '16/04/2000')
# Task, deadline, number of divisions possible
mobile_task_try = MobileTask(task_try, 'november 10th')


# ---------------------------
def test_repr_task():
    """ Tests the correct behaviour of __repr__ for tasks"""

    assert task_try.__repr__() == \
           "Task(name : Try, duration : 10 minutes, difficulty : 5/10)"
    assert fixed_task_try.__repr__() == \
           "FixedTask(name : Try, duration : 10 minutes, difficulty : 5/10)" \
           " begins on : 16/04/2000"
    assert mobile_task_try.__repr__() == "MobileTask(name : Try, duration : 10 minutes," \
                                         " difficulty : 5/10)," \
                                         " to do before november 10th"\
        .format(str(datetime.datetime.now())[:10])


# ---------------------------
def test_eq_task():
    """ Tests the correct behaviour of __eq__ for tasks"""

    assert task_try != Task(0, 'Try 2', 10, 5)
    assert task_try != Task(0, 'Try', 8, 5)
    assert task_try != Task(0, 'Try', 10, 6)

# Tests the optimization program
# schedule_optimized_try = optimize.OptimizedSchedule(schedule_try)
