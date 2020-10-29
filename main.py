"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

import task
import schedule
# import optimize

# It should now display various examples of tasks - To add later to tests.py
task_try = task.Task('Try', 10, 5)  # Name, duration, difficulty
fixed_task_try =\
    task.FixedTask(task_try, '16/04/2000', False)   # Task, beginning_date, Recurring
mobile_task_try = \
    task.MobileTask(task_try, 'november 10th', 'Maths', 3)  # Task, deadline, attached, number of divisions possible

print(task_try)
print(fixed_task_try)
print(mobile_task_try)
print("---------------")

# It should now display : "True, False, False, False" - To add later to tests.py
print(task_try == task_try)
print(task_try == task.Task('Try 2', 10, 5))
print(task_try == task.Task('Try', 8, 5))
print(task_try == task.Task('Try', 10, 6))
print("---------------")

# Tests copy properties - To add later to tests.py
task_dummy = task_try
print(task_dummy)
task_dummy.difficulty = 8
print(task_try == task_dummy)
print("---------------")

# It should now display various examples of tasks - To add later to tests.py
day_try = schedule.Day([None, None, None, task_try, None, task_try, None])
day_try_2 = schedule.Day([None, None, task_try, task_try, None, task_try, None])
day_try_3 = schedule.Day([None, task_try, task_try, task_try, None, task_try, None])
week_try = schedule.Week([day_try, day_try_2])
week_try_2 = schedule.Week([day_try, day_try_3])
schedule_try = schedule.Schedule([week_try, week_try_2])
print(day_try)
print(week_try)
print(schedule_try)
print("---------------")

# Tests the optimization program - To add later to tests.py
# schedule_optimized_try = optimize.OptimizedSchedule(schedule_try)
