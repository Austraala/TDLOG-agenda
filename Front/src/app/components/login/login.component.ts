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


  wait() {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve("I promise to return after one second!");
      }, 6000);
    });
  }


  async login(): Promise<void> {
    console.log('Attempting to connect');
    this.usersApi.loginCheck(`${API_URL}/login_back`, this.user).subscribe(async res => { this.loginValid = await res; }, console.error);
    const value = await this.wait()
    if (this.loginValid === true) {
      localStorage.setItem('username', JSON.stringify({ username: this.user.username }));
      this.router.navigate(['/home']);
    }
    }
}
