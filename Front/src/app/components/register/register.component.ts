import { Component } from '@angular/core';
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
  constructor(private usersApi: UserApiService) { }

  register(): void {
    this.usersApi.registerCheck(`${API_URL}/register`, this.user);
  }
}
