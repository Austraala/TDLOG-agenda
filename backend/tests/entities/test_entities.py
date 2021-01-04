"""
This is a pytest file. To run with pytest

   Jean-Loup Raymond
   ENPC - (c)

"""

import datetime

from ...src.entities.task import Task, FixedTask, MobileTask
from ...src.entities.schedule import Day, Week, Schedule
# from ..algorithm.optimize import

# Defines tested variables
# Name, duration, difficulty
task_try = Task(0, 'Try', 10, 5)
# Task, beginning_date, Recurring
fixed_task_try = FixedTask(task_try, '16/04/2000', False)
# Task, deadline, number of divisions possible
mobile_task_try = MobileTask(task_try, 'november 10th', 3)

day_try = Day()
day_try.content[:6] = [None, None, None, task_try, None, task_try, None]
day_try_2 = Day()
day_try_2.content[:6] = [None, None, task_try, task_try, None, task_try, None]
day_try_3 = Day()
day_try_3.content[:6] = [None, task_try, task_try, task_try, None, task_try, None]
week_try = Week(7)
week_try.days[:1] = [day_try, day_try_2]
week_try_2 = Week(7)
week_try_2.days[:1] = [day_try, day_try_3]
schedule_try = Schedule(3)
schedule_try.weeks[:1] = [week_try, week_try_2]


# ---------------------------
def test_repr_task():
    """ Tests the correct behaviour of __repr__ for tasks"""

    assert task_try.__repr__() == \
           "Task(name : Try, duration : 10 minutes, difficulty : 5/10)"
    assert fixed_task_try.__repr__() == \
           "FixedTask(name : Try, duration : 10 minutes, difficulty : 5/10)" \
           " begins on : 16/04/2000"
    assert mobile_task_try.__repr__() == "MobileTask(name : Try, duration : 10 minutes," \
                                         " difficulty : 5/10)" \
                                         " assigned on {}, to do before november 10th," \
                                         " in 3 times".format(str(datetime.datetime.now())[:10])


# ---------------------------
def test_eq_task():
    """ Tests the correct behaviour of __eq__ for tasks"""

    assert task_try != Task(0, 'Try 2', 10, 5)
    assert task_try != Task(0, 'Try', 8, 5)
    assert task_try != Task(0, 'Try', 10, 6)


# ---------------------------
def test_repr_schedule():
    """ To change to assert once __repr__ is finished """

    day_try.__repr__()
    week_try.__repr__()
    schedule_try.__repr__()

# Tests the optimization program
# schedule_optimized_try = optimize.OptimizedSchedule(schedule_try)
