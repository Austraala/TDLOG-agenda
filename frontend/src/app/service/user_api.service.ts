import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { throwError } from 'rxjs';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/toPromise';
import { User, MobileTask, FixedTask } from '../models/classes.model';

@Injectable()
export class UserApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any): Observable<never> {
    return throwError(err.message || 'Error: Unable to complete request.');
  }

  // GET user by username
  public getUser(url: string, username: string): Observable<User> {
    return this.http.post<User>(url, username).catch(UserApiService._handleError);
  }

  // Call login / logout route in flask
  public loginCheck(url: string, user: User): Observable<boolean> {
    return this.http.post<boolean>(url, user).catch(UserApiService._handleError);
  }

  // Call register route in flask
  public registerCheck(url: string, user: User): Observable<boolean> {
    return this.http.post<boolean>(url, user).catch(UserApiService._handleError);
  }

  // GET list of mobile tasks
  public getMobileTasks(url: string, user: User): Observable<MobileTask[]> {
    return this.http.post<MobileTask[]>(url, user).catch(UserApiService._handleError);
  }

  // POST a mobile task
  public postMobileTask(url: string, mobileTask: MobileTask): Observable<boolean> {
    return this.http.post<boolean>(url, mobileTask).catch(UserApiService._handleError);
  }

  // GET list of mobile tasks
  public getFixedTasks(url: string, user: User): Observable<FixedTask[]> {
    return this.http.post<FixedTask[]>(url, user).catch(UserApiService._handleError);
  }

  // POST a request for the back to attribute Mobile Tasks
  public postPlaceTasks(url: string, user: User, date: Date): Observable<boolean> {
    return this.http.post<boolean>(url, [user, date]).catch(UserApiService._handleError);
  }

  public getDecks(url: string, user: User): Observable<string[]> {
    return this.http.post<string[]>(url, user).catch(UserApiService._handleError);
  }
}
