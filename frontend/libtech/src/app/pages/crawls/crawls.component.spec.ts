import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrawlsComponent } from './crawls.component';

describe('CrawlsComponent', () => {
  let component: CrawlsComponent;
  let fixture: ComponentFixture<CrawlsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrawlsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrawlsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
