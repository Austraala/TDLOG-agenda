import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { UserApiService } from '../../Service/user_api.service';
import { API_URL } from '../../env';

import { User, Task, Schedule } from '../../Models/classes.model';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  user: User = new User("","","","");
  loggedUserSubs: Subscription = new Subscription();
  loggedUser: User = new User("","","","");
  constructor(private usersApi: UserApiService) {}

  ngOnInit() {
      this.user = new User("Archlinux", "Bull", "M", "a@com");
    }

  ngOnDestroy() {
    this.loggedUserSubs.unsubscribe();
  }

  logIn({value}: {value: User}){
      this.user = value;
      this.loggedUserSubs = this.usersApi.logBack(`${API_URL}/login_back`, this.user).subscribe(res => {this.loggedUser = res; }, console.error);
  }

  logOut(user : User){
      this.user = user;
      this.loggedUserSubs = this.usersApi.logBack(`${API_URL}/logout_back`, this.user).subscribe(res => {this.loggedUser = res; }, console.error);
  }
}
