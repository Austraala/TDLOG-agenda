"""
This file defines the class Task for our planning system

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c) 05/10/2020

"""

# Imports
import datetime


class Task:
    """
    We define a Task by its day of assignment, duration, name,
    difficulty and a variety of labels to organize the planning properly
    """

    def __init__(self, name, duration, difficulty):
        """ We get the duration, name, difficulty and labels from the user """

        self.name = name
        self.duration = duration
        self.difficulty = difficulty
        self.labels = []
        self.beginning_date = None

    def __repr__(self):
        """
        Returns
        Task(name : name, duration : duration minutes,
         difficulty : difficulty/10, labels : [labels])
        """

        return "Task(name : " + str(self.name) \
               + ", duration : " + str(self.duration) \
               + " minutes, difficulty : " + str(self.difficulty) \
               + "/10, labels : " + str(self.labels) + ")"

    def __eq__(self, other):
        """ Returns True if everything is the same """
        return (self.name == other.name and self.duration == other.duration
                and self.difficulty == other.difficulty and self.labels == other.labels)


class FixedTask(Task):
    """
    We define a FixedTask class to model properly Tasks
    that have a defined time stamp
    """

    def __init__(self, task, beginning_date, recurring):
        # We call the __init__ function of the class Task
        super().__init__(task.name, task.duration, task.difficulty)

        # We define the beginning date of the task
        self.beginning_date = beginning_date

        # If it is a recurring task, then add a label "recurring" to it
        if recurring:
            self.labels.append("recurring")

    def __repr__(self):
        """
        Returns
        FixedTask(name : name, duration : duration minutes,
        difficulty : difficulty/10, labels : [labels]) begins on : beginning_date
        """

        return "Fixed" + super().__repr__() + " begins on : " + str(self.beginning_date)

    def __eq__(self, other):
        """ Returns True if everything is the same """

        return super().__eq__(other) * (self.beginning_date == other.beginning_date)


class MobileTask(Task):
    """
    We define a MobileTask to properly model Tasks that
    don't have a defined timestamp and can be placed
    """

    def __init__(self, task, deadline, attached, divisions):
        # We call the __init__ function of the class Task
        super().__init__(task.name, task.duration, task.difficulty)

        # We store the time of assignment in the object class
        self.assignment_date = datetime.datetime.now()

        self.deadline = deadline
        self.labels.append(attached)
        self.divisions = divisions

    def __repr__(self):
        """
        Returns
        MobileTask(name : name, duration : duration minutes,
        difficulty : difficulty/10, labels : [labels]) assigned on assignment_date
        to do before deadline, in divisions times
        """
        return "Mobile" + super().__repr__() + " assigned on " + str(self.assignment_date) \
               + ", to do before " + str(self.deadline) + ", in " + str(self.divisions) + " times"

    def __eq__(self, other):
        """ Returns True if everything besides
        assignment_date is the same """
        return (super().__eq__(other) * (self.deadline == other.deadline)
                * (self.divisions == other.divisions))
