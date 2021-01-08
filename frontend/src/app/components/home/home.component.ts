import { Component, OnInit, OnDestroy } from '@angular/core';
import { API_URL } from '../../env';
import { Subscription } from 'rxjs/Subscription';

import { User, Task, MobileTask } from '../../models/classes.model';
import { UserApiService } from '../../service/user_api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  difficulties = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  username = '';
  user: User = new User('', '', '', '');

  task: Task = new Task(this.user, '', 0, 0);
  mobileTask: MobileTask = new MobileTask("date dummy", this.task);

  logoutValid = false;

  mobileTasksListSubs: Subscription = new Subscription();
  mobileTasksList: MobileTask[] = [];

  constructor(private usersApi: UserApiService, private router: Router) { }

  async ngOnInit(): Promise<void> {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    await this.usersApi.getUser(`${API_URL}/user`, this.username).toPromise()
      .then(result => { this.user = result; }, console.error);
    this.mobileTasksListSubs = this.usersApi.getMobileTasks(`${API_URL}/mobile_tasks`, this.user)
      .subscribe(result => { this.mobileTasksList = result; }, console.error);
    this.task.user = this.user;
  }


  addTask(): void {
    console.log(this.user);
    this.usersApi.postMobileTask(`${API_URL}/add_mobile_task`, this.mobileTask).toPromise();
    this.task = new Task(this.user, '', 0, 0);
    this.mobileTask = new MobileTask("date dummy", this.task);
    this.ngOnInit();
  }


  logout(): void {
    console.log('Attempting to disconnect');
    this.usersApi.loginCheck(`${API_URL}/logout_back`, this.user)
      .subscribe(res => { this.logoutValid = res; }, console.error);
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }


  ngOnDestroy(): void {
    this.mobileTasksListSubs.unsubscribe();
  }
}
