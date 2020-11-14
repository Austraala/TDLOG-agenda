import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {throwError} from 'rxjs';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import {User} from '../Models/user.model';

@Injectable()
export class UserApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    return throwError(err.message || 'Error: Unable to complete request.');
  }

  // GET list of public, future events
  public getUsers(url: string): Observable<User[]> {
    return this.http.get<User[]>(url).catch(UserApiService._handleError);
  }
}
