"""
This file contains functions to encrypt and decrypt a password

   Jean-Loup Raymond
   ENPC - (c)

"""


import bcrypt


def encrypt(password):
    salt = bcrypt.gensalt(rounds=16)
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password


def compare(password_try, encrypted_password):
    return bcrypt.checkpw(password_try, encrypted_password)
