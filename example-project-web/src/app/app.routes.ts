import {Routes} from '@angular/router';
import {HomeComponent} from './home/home.component';
import {ExampleFormComponent} from './example-form/example-form.component';
import {ExampleTableComponent} from './example-table/example-table.component';
import {ExampleDialogsComponent} from './example-dialogs/example-dialogs.component';
import {ExampleWebsocketComponent} from './example-websocket/example-websocket.component';
import {loggedInGuard} from './shared/authentication/logged-in.guard';
import {notLoggedInGuard} from './shared/authentication/not-logged-in.guard';
import {LoginComponent} from './login/login.component';
import {LayoutComponent} from './layout/layout.component';

export const routes: Routes = [
    {
        path: '',
        canActivate: [loggedInGuard],
        component: LayoutComponent,
        children: [
            {path: '', redirectTo: 'home', pathMatch: 'full'},
            {path: 'home', component: HomeComponent},
            {path: 'example-form', component: ExampleFormComponent, canActivate: [loggedInGuard]},
            {path: 'example-table', component: ExampleTableComponent, canActivate: [loggedInGuard]},
            {path: 'example-dialogs', component: ExampleDialogsComponent, canActivate: [loggedInGuard]},
            {path: 'example-websockets', component: ExampleWebsocketComponent, canActivate: [loggedInGuard]},]
    },
    {path: 'login', component: LoginComponent, canActivate: [notLoggedInGuard]},
];
