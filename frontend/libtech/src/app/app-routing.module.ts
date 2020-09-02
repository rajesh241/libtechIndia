import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AuthGuard } from '@core/guards/auth.guard';

import { HomeComponent } from '@pages/home/home.component';
import { AdminComponent } from '@pages/admin/admin.component';
import { CrawlsComponent } from '@pages/crawls/crawls.component';
import { LoginComponent } from '@pages/users/components/login/login.component';

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
    canActivate:[AuthGuard]
  },
  {
    path: 'crawls',
    component: CrawlsComponent,
    canActivate:[AuthGuard]
  },
  {
    path: 'login',
    component: LoginComponent,
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
