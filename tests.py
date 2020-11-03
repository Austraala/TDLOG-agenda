"""
This is a pytest file. To run with pytest

   Jean-Loup Raymond
   ENPC - (c)

"""

import datetime

import task
import schedule

# import optimize

# Defines tested variables
# Name, duration, difficulty
task_try = task.Task('Try', 10, 5)
# Task, beginning_date, Recurring
fixed_task_try = task.FixedTask(task_try, '16/04/2000', False)
# Task, deadline, attached, number of divisions possible
mobile_task_try = task.MobileTask(task_try, 'november 10th', 'Maths', 3)
day_try = schedule.Day()
day_try.five_minute_slots[:6] = [None, None, None, task_try, None, task_try, None]
day_try_2 = schedule.Day()
day_try_2.five_minute_slots[:6] = [None, None, task_try, task_try, None, task_try, None]
day_try_3 = schedule.Day()
day_try_3.five_minute_slots[:6] = [None, task_try, task_try, task_try, None, task_try, None]
week_try = schedule.Week()
week_try.days[:1] = [day_try, day_try_2]
week_try_2 = schedule.Week()
week_try_2.days[:1] = [day_try, day_try_3]
schedule_try = schedule.Schedule(3)
schedule_try.weeks[:1] = [week_try, week_try_2]


# ---------------------------
def test_repr_task():
    """ Tests the correct behaviour of __repr__ for tasks"""

    assert task_try.__repr__() == \
           "Task(name : Try, duration : 10 minutes, difficulty : 5/10, labels : [])"
    assert fixed_task_try.__repr__() == \
           "FixedTask(name : Try, duration : 10 minutes, difficulty : 5/10, labels : [])" \
           " begins on : 16/04/2000"
    assert mobile_task_try.__repr__() == "MobileTask(name : Try, duration : 10 minutes," \
                                         " difficulty : 5/10, labels : ['Maths'])" \
                                         " assigned on {}, to do before november 10th," \
                                         " in 3 times".format(str(datetime.datetime.now())[:10])


# ---------------------------
def test_eq_task():
    """ Tests the correct behaviour of __eq__ for tasks"""

    assert task_try != task.Task('Try 2', 10, 5)
    assert task_try != task.Task('Try', 8, 5)
    assert task_try != task.Task('Try', 10, 6)


# ---------------------------
def test_repr_schedule():
    """ To change to assert once __repr__ is finished """

    # print(day_try)
    # print(week_try)
    # print(schedule_try)
    # print("---------------")

# Tests the optimization program
# schedule_optimized_try = optimize.OptimizedSchedule(schedule_try)
