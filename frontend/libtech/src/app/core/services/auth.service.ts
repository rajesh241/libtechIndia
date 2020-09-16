import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() {
    console.log('AuthService.constructor()');
  }

  isAuthenticated() {
    console.log('AuthService.isAuthenticated()');
    return true;
  }

  isLoggedIn() {
    console.log('AuthService.isLoggedIn()');
    return true;
  }
}
