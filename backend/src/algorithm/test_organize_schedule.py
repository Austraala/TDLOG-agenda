"""
This is a pytest file. To run with pytest

   Aaron Fargeon
   Benjamin Roulin
   ENPC - (c)

"""
# pylint: disable=E0401

from Back.src.algorithm.organize_schedule import merge_time_constraints, \
    test_simultaneity  # , smooth_time_constraints, register_constraint


constraint_one_test, constraint_two_test, constraint_three_test, constraint_four_test\
    = [11, 13], [9, 12], [14, 16], [13, 15]
list_constraint_test = [constraint_one_test, constraint_two_test,
                        constraint_three_test, constraint_four_test]


def test_merge_time_constraints():
    """ Tests if the merge time constraints works correctly """

    assert merge_time_constraints(
        list_constraint_test, constraint_one_test, constraint_two_test) == [9, 13]


def test_test_simultaneity():
    """ Tests if the simultaneity check works correctly """

    assert test_simultaneity(constraint_three_test, constraint_four_test)

#   Tests for organize_schedule
