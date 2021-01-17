import { Component, OnInit, OnDestroy, ChangeDetectionStrategy,
  ViewChild, TemplateRef, } from '@angular/core';
import { DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { startOfDay, endOfDay, subDays, addDays,
  endOfMonth, isSameDay, isSameMonth, addHours, addMinutes } from 'date-fns';
import { Subject } from 'rxjs';
import { Subscription } from 'rxjs/Subscription';
import { CalendarEvent, CalendarEventAction,
  CalendarEventTimesChangedEvent, CalendarView,
} from 'angular-calendar';

import { API_URL } from '../../env';
import { User, Task, MobileTask, FixedTask } from '../../models/classes.model';
import { UserApiService } from '../../service/user_api.service';

const colors: any = {
  red: {
    primary: '#ad2121',
    secondary: '#FAE3E3',
  },
  blue: {
    primary: '#1e90ff',
    secondary: '#D1E8FF',
  },
  yellow: {
    primary: '#e3bc08',
    secondary: '#FDF1BA',
  },
};


@Component({
  selector: 'app-home',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  providers:[DatePipe]
})
export class HomeComponent implements OnInit, OnDestroy {
  constructor(private usersApi: UserApiService, private router: Router, private datePipe : DatePipe) { }
  difficulties = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  username = '';
  user: User = new User('', '', '', '');

  task: Task = new Task(this.user, '', 0, 0);
  mobileTask: MobileTask = new MobileTask(this.datePipe.transform(new Date(), 'yyyy-MM-dd'), this.task);

  logoutValid = false;

  mobileTasksListSubs: Subscription = new Subscription();
  mobileTasksList: MobileTask[] = [];
  fixedTasksListSubs: Subscription = new Subscription();
  fixedTasksList: FixedTask[] = [];

  refresh: Subject<any> = new Subject();

  events: CalendarEvent[] = [];

  activeDayIsOpen = true;

  view: CalendarView = CalendarView.Month;

  CalendarView = CalendarView;

  viewDate: Date = new Date();

  async ngOnInit(): Promise<void> {
    await this.load()

    for (let mobileTask of this.mobileTasksList) {
        this.events = [
        ...this.events,
        {
          title: mobileTask.task!.name,
          start: startOfDay(new Date()),
          end: endOfDay(new Date()),
          color: colors.blue,
          draggable: true,
          resizable: {
            beforeStart: true,
            afterEnd: true,
          }
        }
        ];
        console.log(this.events)
        }

    for (let fixedTask of this.fixedTasksList) {
        this.events = [
        ...this.events,
        {
          title: fixedTask.task!.name,
          start: new Date(fixedTask.start),
          end: new Date(addMinutes(new Date(fixedTask.start), fixedTask.task!.duration)),
          color: colors.red,
          draggable: false,
          resizable: {
            beforeStart: false,
            afterEnd: false,
          }
        }
        ];
        console.log(fixedTask)
        }
    this.task.user = this.user;
    this.refresh.next();
    this.refresh.next()
  }

  async load(): Promise<void> {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    await this.usersApi.getUser(`${API_URL}/user`, this.username).toPromise().then(result => { this.user = result; });
    await this.usersApi.getMobileTasks(`${API_URL}/mobile_tasks`, this.user).toPromise().then(result => this.mobileTasksList = result);
    await this.usersApi.getFixedTasks(`${API_URL}/fixed_tasks`, this.user).toPromise().then(result => this.fixedTasksList = result);
  }

  addTask(): void {
    console.log(this.user);
    this.usersApi.postMobileTask(`${API_URL}/add_mobile_task`, this.mobileTask).toPromise();
    this.events = [
      ...this.events,
      {
        title: this.task.name,
        start: startOfDay(new Date()),
        end: endOfDay(new Date()),
        color: colors.blue,
        draggable: true,
        resizable: {
          beforeStart: true,
          afterEnd: true,
        },
      },
    ];
    this.mobileTasksList = [...this.mobileTasksList, this.mobileTask]
    this.task = new Task(this.user, '', 0, 0);
    this.mobileTask = new MobileTask(this.datePipe.transform(new Date(), 'yyyy-MM-dd'), this.task);
    this.refresh.next()
  }


  logout(): void {
    console.log('Attempting to disconnect');
    this.usersApi.loginCheck(`${API_URL}/logout_back`, this.user)
      .subscribe(res => { this.logoutValid = res; }, console.error);
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }

  eventTimesChanged({
    event,
    newStart,
    newEnd,
  }: CalendarEventTimesChangedEvent): void {
    this.events = this.events.map((iEvent) => {
      if (iEvent === event) {
        return {
          ...event,
          start: newStart,
          end: newEnd,
        };
      }
      return iEvent;
    });

  }


  deleteEvent(eventToDelete: CalendarEvent): void {
    this.events = this.events.filter((event) => event !== eventToDelete);
  }

  setView(view: CalendarView): void {
    this.view = view;
  }

  closeOpenMonthViewDay(): void {
    this.activeDayIsOpen = false;
  }

  ngOnDestroy(): void {
    this.mobileTasksListSubs.unsubscribe();
  }
}

