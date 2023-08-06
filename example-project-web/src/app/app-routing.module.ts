import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full', data: {routeName: ''}},
  {
    path: 'home',
    component: DashboardLayoutComponent,
    canActivate: [LoggedInGuard],
    children: [
      {path: '', component: HomePageComponent, pathMatch: 'full', data: {routeName: 'home'}},
    ],
  },
  {
    path: 'login',
    canActivate: [LoggedOutGuard],
    loadChildren: () => import('./login/login.module').then(m => m.LoginModule)
  },
  {
    path: 'websockets-example',
    component: DashboardLayoutComponent,
    canActivate: [LoggedInGuard],
    loadChildren: () => import('./websockets-example/websockets-example.module').then(m => m.WebsocketsExampleModule)
  },
  {
    path: 'table-example',
    component: DashboardLayoutComponent,
    canActivate: [LoggedInGuard],
    loadChildren: () => import('./table-example/table-example.module').then(m => m.TableExampleModule)
  },
  {
    path: 'form-example',
    component: DashboardLayoutComponent,
    canActivate: [LoggedInGuard],
    loadChildren: () => import('./form-example/form-example.module').then(m => m.FormExampleModule)
  },
  {
    path: 'dialogs-example',
    component: DashboardLayoutComponent,
    canActivate: [LoggedInGuard],
    loadChildren: () => import('./dialogs-example/dialogs-example.module').then(m => m.DialogsExampleModule)
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
