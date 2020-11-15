// This file defines the class Task for our planning system on the front end

import {User} from './user.model';
import {Day} from './schedule.model';

export class Task {
  constructor(
    public user: User,
    public gender: string,
    public name: string,
    public duration: number,
    public difficulty: number,
    public mobileTask: MobileTask,
    public fixedTask: FixedTask,
    public id?: number,
    public userId?: number,
  ) { }
}

export class MobileTask {
  constructor(
    public beginningDate: number,
    public recurring: number,
    public task: Task,
    public day: Day,
    public id?: number,
  ) { }
}

export class FixedTask {
  constructor(
    public deadline: number,
    public division: number,
    public task: Task,
    public id?: number,
  ) { }
}
