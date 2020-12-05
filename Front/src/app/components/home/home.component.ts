import { Component, OnInit } from '@angular/core';
import { API_URL } from '../../env';
import { Subscription } from 'rxjs/Subscription';

import { User } from '../../models/classes.model';
import { Task } from '../../models/classes.model';
import { UserApiService } from '../../service/user_api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  username = '';
  user: User = new User('', '', '', '');
  logoutValid = false;
  tasksListSubs: Subscription = new Subscription();
  tasksList: Task[] = [];

  constructor(private usersApi: UserApiService, private router: Router) { }

  async ngOnInit(): Promise<void> {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    await this.usersApi.getUser(`${API_URL}/user`, this.username).toPromise()
    .then(result => { this.user = result; }, console.error);
    this.tasksListSubs = this.usersApi.getTasks(`${API_URL}/tasks`, this.user)
    .subscribe(result => { this.tasksList = result; }, console.error);
  }


  logout(): void {
    console.log('Attempting to disconnect');
    this.usersApi.loginCheck(`${API_URL}/logout_back`, this.user)
      .subscribe(res => { this.logoutValid = res; }, console.error);
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }


  ngOnDestroy(): void {
    this.tasksListSubs.unsubscribe();
  }
}
