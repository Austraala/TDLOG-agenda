"""
This file contains functions to encrypt and decrypt a password

   Jean-Loup Raymond
   ENPC - (c)

"""


import bcrypt


def encrypt(password):
    """ Hashes the password to store it in the database """

    salt = bcrypt.gensalt(rounds=16)
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def compare(password, encrypted_password):
    """
    Check if the encrypted password is a possible hash from an original password
    """

    return bcrypt.checkpw(password, encrypted_password)
