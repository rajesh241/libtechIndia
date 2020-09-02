export class User {
  id: number;
  email: string;
  name: string;
  avatar: File;
  is_active: boolean;
  is_locked: boolean;
  provider: string;
  avatar_url: string;
  user_role: string;
  login_attempt_count: number;
  username: string;
  phone: string;

  /*
  constructor(private id: number,
              public email: string,
              public: name: string,
             ) {
  }
  */
}
