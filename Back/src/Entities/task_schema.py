"""
This file defines the marshmallow schemas for Task for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable= E0402

from marshmallow import Schema, fields
from .user import User
from .task import Task, FixedTask, MobileTask
from .schedule import Day


class TaskSchema(Schema):
    """ Marshmallow class to allow json manipulation of task"""
    id = fields.Number()
    user_id = fields.Number()
    user = fields.Nested(User)
    name = fields.String()
    duration = fields.Integer()
    difficulty = fields.Integer()
    fixed_task = fields.List(fields.Nested(FixedTask))
    mobile_task = fields.List(fields.Nested(MobileTask))


class FixedTaskSchema(Schema):
    """ Marshmallow class to allow json manipulation of fixed task"""
    id = fields.Number()
    beginning_date = fields.Number()
    recurring = fields.Boolean()
    task = fields.Nested(Task)
    day = fields.Nested(Day)


class MobileTaskSchema(Schema):
    """ Marshmallow class to allow json manipulation of fixed task"""
    id = fields.Number()
    deadline = fields.Number()
    division = fields.Number()
    task = fields.Nested(Task)
