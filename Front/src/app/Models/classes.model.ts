// This file defines the class User for our planning system on the front end

export class User {
  constructor(
    public username: string,
    public password: string,
    public gender: string,
    public email: string,
    public tasks?: Task,
    public schedule?: Schedule,
    public id?: number,
  ) { }
}

export class Task {
  constructor(
    public user: User,
    public name: string,
    public duration: number,
    public difficulty: number,
    public mobileTask?: MobileTask,
    public fixedTask?: FixedTask,
    public id?: number,
    public userId?: number,
  ) { }
}

export class MobileTask {
  constructor(
    public beginningDate: number,
    public recurring: number,
    public task?: Task,
    public id?: number,
  ) { }
}

export class FixedTask {
  constructor(
    public deadline: number,
    public division: number,
    public task?: Task,
    public day?: Day,
    public id?: number,
  ) { }
}

export class Schedule {
  constructor(
    public user: User,
    public weeks?: Week,
    public id?: number,
    public userId?: number,
  ) { }
}

export class Week {
  constructor(
    public schedule: Schedule,
    public days?: Day,
    public id?: number,
    public scheduleId?: number,
  ) { }
}

export class Day {
  constructor(
    public week: Week,
    public fixedTasks?: FixedTask,
    public id?: number,
    public weekId?: number,
    public fixedTaskId?: number,
  ) { }
}
