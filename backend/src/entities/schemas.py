"""
This file defines the marshmallow schemas for our planning system

   Jean-Loup Raymond
   ENPC - (c)

"""
# pylint: disable= E0402

from marshmallow import Schema, fields


class UserSchema(Schema):
    """ Marshmallow class to allow json manipulation of user"""
    id = fields.Number()
    username = fields.String()
    gender = fields.String()
    email = fields.String()


class TaskSchema(Schema):
    """ Marshmallow class to allow json manipulation of task"""
    id = fields.Number()
    user_id = fields.Number()
    user = fields.Nested(UserSchema)
    name = fields.String()
    duration = fields.Integer()
    difficulty = fields.Integer()


UserSchema.task = fields.Nested(TaskSchema)


class FixedTaskSchema(Schema):
    """ Marshmallow class to allow json manipulation of fixed task"""
    id = fields.Number()
    start = fields.Date()
    task = fields.Nested(TaskSchema)


TaskSchema.fixed_task = fields.List(fields.Nested(FixedTaskSchema))


class MobileTaskSchema(Schema):
    """ Marshmallow class to allow json manipulation of fixed task"""
    id = fields.Number()
    deadline = fields.Date()
    task = fields.Nested(TaskSchema)


TaskSchema.mobile_task = fields.List(fields.Nested(MobileTaskSchema))


class ScheduleSchema(Schema):
    """ Marshmallow class to allow json manipulation of schedule"""
    id = fields.Number()
    user_id = fields.Number()
    user = fields.Nested(UserSchema)


UserSchema.schedule = fields.Nested(ScheduleSchema)


class WeekSchema(Schema):
    """ Marshmallow class to allow json manipulation of week"""
    id = fields.Number()
    schedule_id = fields.Number()
    schedule = fields.Nested(ScheduleSchema)


ScheduleSchema.weeks = fields.List(fields.Nested(WeekSchema))


class DaySchema(Schema):
    """ Marshmallow class to allow json manipulation of day"""
    id = fields.Number()
    week_id = fields.Number()
    week = fields.Nested(WeekSchema)
    fixed_task_id = fields.Number()
    fixed_tasks = fields.List(fields.Nested(FixedTaskSchema))


FixedTaskSchema.day = fields.Nested(DaySchema)
WeekSchema.days = fields.List(fields.Nested(DaySchema))

