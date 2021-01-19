import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class AuthGuard implements CanActivate {

  constructor(
    private router: Router
  ) { }

  // Condition to be able to see Home and Cards
  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {
    // Check if the user is connected
    const alreadyLoggedIn = !(localStorage.getItem('username') === null);

    if (!alreadyLoggedIn) {
      // Redirection to the login page
      console.log('You are not connected');
      this.router.navigate(['/login']);
    }
    return alreadyLoggedIn;
  }
}
