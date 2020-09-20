export class User {
  id: number;
  name: string;
  username: string;
  email: string;
  phone: string;
  user_role: string;
  login_attempt_count: number;
  provider: string;
  avatar: File;
  avatar_url: string;
  is_active: boolean;
  is_locked: boolean;

  private _token: string;
  private _tokenExpirationDate: Date

  /*
  constructor(private id: number,
              public email: string,
              public: name: string,
             ) {
  }

  set token(token) {
  this._token = token;
  }
  */

  get token() {
    if (!this._tokenExpirationDate || new Date() > this._tokenExpirationDate) {
      return null;
    }
    return this._token;
  }
}
