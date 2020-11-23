import { Component, OnInit } from '@angular/core';
import { API_URL } from '../../env';
import { User } from '../../models/classes.model';

import { UserApiService } from '../../service/user_api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  username = '';
  logoutValid = false;

  constructor(private usersApi: UserApiService, private router: Router) { }

  ngOnInit(): void {
  }

  getLogin(): string {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    return this.username['username' as any];
  }

  logout(): void {
    console.log('Attempting to disconnect');
    this.username = this.getLogin();
    this.usersApi.loginCheck(`${API_URL}/logout_back`, new User(this.username, '', '', ''))
      .subscribe(res => { this.logoutValid = res; }, console.error);
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }

}
