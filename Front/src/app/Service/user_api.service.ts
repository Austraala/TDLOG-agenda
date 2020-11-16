import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {throwError} from 'rxjs';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/toPromise';
import {User} from '../Models/classes.model';

@Injectable()
export class UserApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return throwError(err.message || 'Error: Unable to complete request.');
  }

  // GET list of users
  public getUsers(url: string): Observable<User[]> {
    return this.http.get<User[]>(url).catch(UserApiService._handleError);
  }

  // Call login / logout route in flask
  public logBack(url: string, user: User): Observable<User> {
    return this.http.post<User>(url, user).catch(UserApiService._handleError);
    }
}
