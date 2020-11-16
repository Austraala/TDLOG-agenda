"""
This is a pytest file. To run with pytest

   Aaron Fargeon
   ENPC - (c)

"""

from Algorithm.crypto import encrypt, compare
from Algorithm.optimize import merge_time_constraints, \
    test_simultaneity  # , smooth_time_constraints, register_constraint

password_test = "password_test"
encrypted_test = b'$2b$16$r0ZiH4AInwwWyX2rEodRE.0dYzPKEda8N41ZsK4lIq/UavRFfQcV6'


def test_encrypt():
    assert encrypt(password_test) == encrypted_test


def test_compare():
    assert compare(encrypt(password_test), encrypted_test)


constraint_1_test, constraint_2_test, constraint_3_test, constraint_4_test = [11, 13], [9, 12], [14, 16], [13, 15]
list_constraint_test = [constraint_1_test, constraint_2_test, constraint_3_test, constraint_4_test]


def test_merge_time_constraints():
    assert merge_time_constraints(constraint_1_test, constraint_2_test) == [9, 13]


def test_test_simultaneity():
    assert test_simultaneity(constraint_1_test, constraint_2_test)
