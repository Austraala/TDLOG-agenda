"""
This file defines the marshmallow schemas for Schedule for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable= E0402

from marshmallow import Schema, fields
from .user import User
from .task import FixedTask
from .schedule import Schedule, Week, Day


class ScheduleSchema(Schema):
    """ Marshmallow class to allow json manipulation of schedule"""
    id = fields.Number()
    user_id = fields.Number()
    user = fields.Nested(User)
    weeks = fields.List(fields.Nested(Week))


class WeekSchema(Schema):
    """ Marshmallow class to allow json manipulation of week"""
    id = fields.Number()
    schedule_id = fields.Number()
    schedule = fields.Nested(Schedule)
    days = fields.List(fields.Nested(Day))


class DaySchema(Schema):
    """ Marshmallow class to allow json manipulation of day"""
    id = fields.Number()
    week_id = fields.Number()
    week = fields.Nested(Week)
    task_id = fields.Number()
    fixed_tasks = fields.List(fields.Nested(FixedTask))
