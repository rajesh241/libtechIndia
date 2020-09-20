import { Injectable } from '@angular/core';

import { User } from '@pages/users/models/user';

export interface AuthData {

}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private user: User;

  constructor() {
    console.log('AuthService.constructor()');
  }

  isAuthenticated() {
    // console.log('AuthService.isAuthenticated()');
    return true;
  }

  isLoggedIn() {
    console.log('AuthService.isLoggedIn()');
    return true;
  }
}
