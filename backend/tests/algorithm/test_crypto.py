"""
This is a pytest file. To run with pytest

   Aaron Fargeon
   Benjamin Roulin
   ENPC - (c)

"""
# pylint: disable=E0401


from ...src.algorithm.crypto import encrypt, compare

PASSWORD_TEST = "password_test"
ENCRYPTED_TEST = b'$2b$16$r0ZiH4AInwwWyX2rEodRE.0dYzPKEda8N41ZsK4lIq/UavRFfQcV6'


def test_compare():
    """ Tests if the compare function works correctly """

    assert not compare(encrypt(PASSWORD_TEST), ENCRYPTED_TEST)
