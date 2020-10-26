"""
This is the main file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

import task

task_try = task.Task('Try', 10, 5)
print(task_try)
print(task.FixedTask(task_try, '16/04/2000', False))
print(task.MobileTask(task_try, 'november 10th', 'Maths', 3))
