import {Component, OnInit, OnDestroy} from '@angular/core';
import {Subscription} from 'rxjs/Subscription';
import {UserApiService} from './Service/user_api.service';
import {User} from './Models/user.model';
import {API_URL} from './env';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  usersListSubs: Subscription = new Subscription();
  usersList: User[] = [];

  constructor(private usersApi: UserApiService) {
  }

  ngOnInit() {
    this.usersListSubs = this.usersApi.getUsers(`${API_URL}/users`).subscribe(res => {this.usersList = res; }, console.error);
  }

  ngOnDestroy() {
    this.usersListSubs.unsubscribe();
  }
}
