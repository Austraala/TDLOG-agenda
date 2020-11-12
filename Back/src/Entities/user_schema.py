"""
This file defines the marshmallow schemas for User for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable= E0402

from marshmallow import Schema, fields
from .task import Task
from .schedule import Schedule


class UserSchema(Schema):
    """ Marshmallow class to allow json manipulation of user"""
    id = fields.Number()
    beginning_date = fields.Number()
    recurring = fields.Boolean()
    task = fields.Nested(Task)
    schedule = fields.Nested(Schedule)
