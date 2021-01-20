"""
This is a pytest file. To run with pytest

   Aaron Fargeon
   Benjamin Roulin
   ENPC - (c)

"""
# pylint: disable=E0401

from ...src.algorithm.toolbox_organize_schedule import Constraint, sort_time_constraints

from ...src.algorithm.entities.task import Task, FixedTask, MobileTask

from ...src.algorithm.interface_organize_schedule import get_constraints

constraint_one_test = Constraint("Constraint_1", False, False, False, False, 30, [2021, 6, 8, 900], True, False)
constraint_two_test = Constraint("Constraint_2", False, False, False, False, 60, [2021, 6, 8, 540], True, False)
constraint_three_test = Constraint("Constraint_3", False, False, False, False, 45, [2021, 6, 8, 600], True, False)
constraint_four_test = Constraint("Constraint_4", False, False, False, False, 60, [2021, 6, 8, 600], True, False)

list_constraints = [constraint_one_test, constraint_two_test, constraint_three_test, constraint_four_test]

task_one_test = MobileTask(
    
)
task_two_test = MobileTask()
task_three_test = MobileTask()
task_four_test = MobileTask()


def test_sort_time_constraints():
    """
    Tests is sort_time_constraints sorts the function properly.
    :return:
    """
    assert sort_time_constraints(list_constraints) == [constraint_two_test,
                                                       constraint_three_test,
                                                       constraint_four_test,
                                                       constraint_one_test]

def get_constraints()
    """
    
    :return: 
    """