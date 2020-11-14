// This file defines the class User for our planning system on the front end

import {Task} from './task.model';
import {Schedule} from './schedule.model';

export class User {
  constructor(
    public username: string,
    public gender: string,
    public email: string,
    public tasks: Task,
    public schedule: Schedule,
    public id?: number,
  ) { }
}
