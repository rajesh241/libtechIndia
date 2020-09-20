import { Component } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';

import { AuthService } from '@core/services/auth.service';  // FIXME - confirm if this is required here

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  loginForm = this.fb.group({
    email: [
      null, Validators.compose([
        Validators.required, Validators.pattern('[^@]*@[^@]*')
      ])
    ],
    password: [
      null, Validators.compose([
        Validators.required, Validators.minLength(8)
      ]),
    ]
  });

  constructor(private fb: FormBuilder, private authService: AuthService) {
    console.log(`LoginComponent.constructor()`);
  }

  onSubmit() {
    console.log(`LoginComponent.onSubmit()`, this.loginForm);
  }
}
