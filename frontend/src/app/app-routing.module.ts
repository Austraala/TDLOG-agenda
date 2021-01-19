import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { CardsComponent } from './components/cards/cards.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { AuthGuard } from './service/auth/auth.guard';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },  // root redirects to login page
  {
    path: 'login',
    component: LoginComponent // Login calls LoginComponent
  },
  {
    path: 'home',
    canActivate: [AuthGuard],
    component: HomeComponent // Home calls HomeComponent if logged in, LoginComponent instead
  },
  {
    path: 'cards',
    canActivate: [AuthGuard],
    component: CardsComponent // Cards calls CardsComponent if logged in, LoginComponent instead
  },
  { path: 'register', component: RegisterComponent }, // Register calls RegisterComponent
  { path: '**', redirectTo: '/login' } // Everything else goes on LoginComponent
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
