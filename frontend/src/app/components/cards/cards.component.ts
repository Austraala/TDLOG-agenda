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

  // What User is logged in
  username = '';
  user: User = new User('', '', '', '');

  // True if user was correctly logged in and can log out
  logoutValid = false;

  // Will contain decks from backend - Not yet implemented
  decksListSubs: Subscription = new Subscription();
  decksList: string[] = [];

  // Deck name from html form
  deckName = '';

  // On load / reload of the component
  ngOnInit(): void {
    // To avoid unnecessary async ngOnInit
    this.load();
  }

  // Loads username token from cache, then gets the user from backend
  async load(): Promise<void> {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    await this.usersApi.getUser(`${API_URL}/user`, this.username).toPromise().then(result => { this.user = result; });
  }

  // Creates an anki deck via ankiweb - should create a copy in db (not yet implemented)
  async createAnkiDeck(): Promise<void> {
    this.decksList = [];
    await this.usersApi.postDeck(`${API_URL}/create`, this.deckName).toPromise()
      .then(result => { this.decksList = [...this.decksList, result]; });
    this.ngOnInit();
  }

  // Check if the user is logged in, then removes token from cache, and redirects to log in page
  logout(): void {
    console.log('Attempting to disconnect');
    this.usersApi.loginCheck(`${API_URL}/logout_back`, this.user)
      .subscribe(res => { this.logoutValid = res; }, console.error);
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }

  // Stop subscriptions
  ngOnDestroy(): void {
    this.decksListSubs.unsubscribe();
  }
}
