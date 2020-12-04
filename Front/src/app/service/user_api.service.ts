import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { throwError } from 'rxjs';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/toPromise';
import { User } from '../models/classes.model';

@Injectable()
export class UserApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any): Observable<never> {
    return throwError(err.message || 'Error: Unable to complete request.');
  }

  // GET list of users
  public getUsers(url: string): Observable<User[]> {
    return this.http.get<User[]>(url).catch(UserApiService._handleError);
  }

  // Call login / logout route in flask
  public loginCheck(url: string, user: User): Observable<boolean> {
    return this.http.post<boolean>(url, user).catch(UserApiService._handleError);
    }

  public registerCheck(url: string, user: User): Observable<boolean> {
    return this.http.post<boolean>(url, user).catch(UserApiService._handleError);
  }
}
