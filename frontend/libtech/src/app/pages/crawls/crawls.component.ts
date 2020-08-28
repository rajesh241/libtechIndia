import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-crawls',
  templateUrl: './crawls.component.html',
  styleUrls: ['./crawls.component.scss']
})
export class CrawlsComponent implements OnInit {

  constructor() {
    console.log(`CrawlsComponent.constructor()`);
  }

  ngOnInit(): void {
  }

}
