import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { UserApiService } from './service/user_api.service';
import { User } from './models/classes.model';
import { API_URL } from './env';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  usersListSubs: Subscription = new Subscription();
  usersList: User[] = [];
  loggedUserSubs: Subscription = new Subscription();
  loggedUser: User = new User('', '', '', '');

  constructor(private usersApi: UserApiService, private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.usersListSubs = this.usersApi.getUsers(`${API_URL}/users`).subscribe(res => { this.usersList = res; }, console.error);
    this.route.queryParams.subscribe(params => {
      this.loggedUser = params.loggedUser;
    });
  }

  ngOnDestroy(): void {
    this.usersListSubs.unsubscribe();
  }
}
