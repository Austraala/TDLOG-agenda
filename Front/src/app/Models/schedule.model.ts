// This file defines the class Task for our planning system on the front end

import {User} from './user.model';
import {FixedTask} from './task.model';

export class Schedule {
  constructor(
    public user: User,
    public weeks: Week,
    public id?: number,
    public userId?: number,
  ) { }
}

export class Week {
  constructor(
    public schedule: Schedule,
    public days: Day,
    public id?: number,
    public scheduleId?: number,
  ) { }
}

export class Day {
  constructor(
    public week: Week,
    public fixedTasks: FixedTask,
    public id?: number,
    public weekId?: number,
    public fixedTaskId?: number,
  ) { }
}
