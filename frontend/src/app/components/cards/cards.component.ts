import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs/Subscription';
import { API_URL } from '../../env';
import { User } from '../../models/classes.model';
import { UserApiService } from '../../service/user_api.service';

@Component({
  selector: 'app-cards',
  templateUrl: './cards.component.html',
  styleUrls: ['./cards.component.css']
})
export class CardsComponent implements OnInit, OnDestroy {

  constructor(private usersApi: UserApiService, private router: Router) { }

  username = '';
  user: User = new User('', '', '', '');

  logoutValid = false;

  decksListSubs: Subscription = new Subscription();
  decksList: string[] = [];

  deckName: string = "";

  ngOnInit(): void {
    this.load();
  }

  ngOnDestroy(): void {
    this.decksListSubs.unsubscribe();
  }

  async load(): Promise<void> {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    await this.usersApi.getUser(`${API_URL}/user`, this.username).toPromise().then(result => { this.user = result; });
  }

  logout(): void {
    console.log('Attempting to disconnect');
    this.usersApi.loginCheck(`${API_URL}/logout_back`, this.user)
      .subscribe(res => { this.logoutValid = res; }, console.error);
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }

  async createAnkiDeck(): Promise<void> {
    this.decksList= [];
    await this.usersApi.postDeck(`${API_URL}/create`, this.deckName).toPromise().then(result => {this.decksList = [...this.decksList, result];});
    this.ngOnInit();
    }
  }
