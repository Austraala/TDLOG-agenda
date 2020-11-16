import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { UserApiService } from '../../Service/user_api.service';
import { API_URL } from '../../env';
import { Router } from '@angular/router';

import { User, Task, Schedule } from '../../Models/classes.model';

@Component({
  selector: 'app-log-in',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit, OnDestroy {
  user: User = new User('', '', '', '');
  loginValidSubs: Subscription = new Subscription();
  loginValid = false;
  constructor(private usersApi: UserApiService, private router: Router) {
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.loginValidSubs.unsubscribe();
  }

  login(): void {
    console.log('Attempting to connect');
    this.usersApi.loginCheck(`${API_URL}/login_back`, this.user).subscribe(res => { this.loginValid = res; }, console.error);
    if (this.loginValid === true) {
      console.log(this.user.username);
      localStorage.setItem('username', JSON.stringify({ username: this.user.username }));
      this.router.navigate(['/home']);
    }
  }
}
