import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  username = '';

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  getLogin(): string {
    this.username = JSON.parse(localStorage.getItem('username') || '{}');
    return this.username['username' as any];
  }

  logout(): void {
    console.log('Attempting to disconnect');
    localStorage.removeItem('username');
    this.router.navigate(['/login']);
  }

}
