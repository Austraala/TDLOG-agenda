// This file defines the class User for our planning system on the front end

export class User {
  constructor(
    public username: string,
    public password: string,
    public gender: string,
    public email: string,
    public tasks?: Task,
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

export class FixedTask {
  constructor(
    public start: Date,
    public task?: Task,
    public id?: number,
  ) { }
}

export class MobileTask {
  constructor(
    public deadline: string | null,
    public task?: Task,
    public id?: number,
  ) { }
}
