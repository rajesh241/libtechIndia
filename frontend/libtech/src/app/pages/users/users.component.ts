import { Component, OnInit } from '@angular/core';

import { User } from './models/user';

const USER: User = JSON.parse(`{
"id": 3,
"email": "mr.mynk@gmail.com",
"name": "Mayank Rungta",
"avatar": null,
"is_active": false,
"is_locked": false,
"provider": "what's this?",
"avatar_url": "http://mayankrungta.in/wp-content/uploads/2011/07/MynkProfileHindu-320x213.jpg",
"user_role": "student",
"login_attempt_count": 0,
"username": "mynk",
"phone": "7019628701"
}`);


@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})

export class UsersComponent implements OnInit {
  public users: User[] = [];
  constructor() {
    console.log(`UsersComponent.constructor()`);
    // let user = new User(USER);
    this.users.push(USER);
    console.log(`UsersComponent.constructor() users = `, this.users);
  }

  ngOnInit(): void {
  }

}
