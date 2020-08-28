import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from '@pages/home/home.component';
import { AdminComponent } from '@pages/admin/admin.component';
import { CrawlsComponent } from '@pages/crawls/crawls.component';

const routes: Routes = [
  /* is redirect better? FIXME
  {
    path: '',
    component: HomeComponent
  },
  */
  {
    path: 'home',
    component: HomeComponent
  },
  {
    path: 'admin',
    component: AdminComponent,
  },
  {
    path: 'crawls',
    component: CrawlsComponent,
  },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
