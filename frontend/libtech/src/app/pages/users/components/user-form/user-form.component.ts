import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

import { Observable, Subscription } from 'rxjs';
import { map, filter, tap, shareReplay } from 'rxjs/operators';

@Component({
  selector: 'user-form',
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.scss']
})
export class UserFormComponent implements OnInit, OnDestroy {
  public action: string = 'Create';

  private formSubscription: Subscription;
  private formValues$: Observable<FormGroup>;

  userForm = this.fb.group({
    company: null,
    firstName: [null, Validators.required],
    lastName: [null, Validators.required],
    address: [null, Validators.required],
    address2: null,
    city: [null, Validators.required],
    state: [null, Validators.required],
    postalCode: [null, Validators.compose([
      Validators.required, Validators.minLength(5), Validators.maxLength(5)])
    ],
    shipping: ['free', Validators.required]
  });

  usrForm = this.fb.group({
    name: [null, Validators.required],
    email: [null, Validators.compose([
      Validators.required, Validators.pattern('[^@]*@[^@]*')
    ])
           ],
    phone: [null, Validators.compose([
      Validators.required, Validators.minLength(10), Validators.maxLength(10)])
           ],
    user_role: [null, Validators.required],
    avatar: [null, Validators.required],
    city: [null, Validators.required],
    state: [null, Validators.required],
    shipping: ['free', Validators.required]
  });
  hasUnitNumber = false;

  states = [
    {name: 'Alabama', abbreviation: 'AL'},
    {name: 'Alaska', abbreviation: 'AK'},
    {name: 'American Samoa', abbreviation: 'AS'},
    {name: 'Arizona', abbreviation: 'AZ'},
    {name: 'Arkansas', abbreviation: 'AR'},
    {name: 'California', abbreviation: 'CA'},
    {name: 'Colorado', abbreviation: 'CO'},
    {name: 'Connecticut', abbreviation: 'CT'},
    {name: 'Delaware', abbreviation: 'DE'},
    {name: 'District Of Columbia', abbreviation: 'DC'},
  ];

  constructor(private fb: FormBuilder) {
    console.log(`UserFormComponent.constructor()`, fb);
    this.formValues$ = this.userForm.valueChanges
      .pipe(
        map(data => {
          data.is_active = false;
          data.is_locked = false;
          data.comment = data.comment.replace(/<(?:.|\n)*?>/gm, '');
          data.lastUpdatedTimeStamp = new Date();
          return data;
        }),
        shareReplay()
      );
  }

  ngOnInit() {
    console.log(`UserFormComponent.onInit()`);
    this.formSubscription = this.formValues$
      .subscribe(console.log);
  }

  ngOnDestroy() {
    console.log(`UserFormComponent.onDestroy()`);
    this.formSubscription.unsubscribe();
  }

  onSubmit() {
    alert('Thanks!');
    console.log(`UserFormComponent.onSubmit()`, this.userForm);
  }
}
