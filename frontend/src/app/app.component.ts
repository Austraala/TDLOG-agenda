import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs/Subscription';
import { UserApiService } from './service/user_api.service';
import { User } from './models/classes.model';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'app';
  loggedUserSubs: Subscription = new Subscription();
  loggedUser: User = new User('', '', '', '');

  constructor(private usersApi: UserApiService, private router: Router, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.loggedUser = params.loggedUser;
    });
  }

  ngOnDestroy(): void {
    this.loggedUserSubs.unsubscribe();
  }
}
