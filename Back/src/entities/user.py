"""
This file defines the class User for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable=E1101

# Imports

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """ We define the class User """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    gender = Column(String(1))
    email = Column(String)
    tasks = None

    def __init__(self, username, password, gender, email):
        """ We set up an user """

        self.username = username
        self.password = password
        self.gender = gender
        self.email = email
        self.tasks = []

    def __repr__(self):
        return str(self.username)

    def __eq__(self, other):
        """
        2 Users are equal if their username is the same
        """
        return self.username == other.username
