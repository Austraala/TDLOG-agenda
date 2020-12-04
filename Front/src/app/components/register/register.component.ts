import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { UserApiService } from '../../service/user_api.service';
import { User } from '../../models/classes.model';
import { API_URL } from '../../env';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  genders = ['M', 'F',
    'Alligator', 'Archlinux User'];

  user: User = new User('', '', '', '');
  registerValid = true;
  constructor(private usersApi: UserApiService, private router: Router) { }

  async register(): Promise<void>  {
    await this.usersApi.registerCheck(`${API_URL}/register`, this.user).toPromise().then(registered => { this.registerValid = registered });
    if (this.registerValid) {
      this.router.navigate(['/home']);
    }
  }
}
