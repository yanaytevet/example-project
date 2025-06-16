import {Routes} from '@angular/router';
import {loggedInGuard} from './shared/authentication/logged-in.guard';
import {notLoggedInGuard} from './shared/authentication/not-logged-in.guard';
import {LayoutComponent} from './layout/layout.component';

export const routes: Routes = [
    {
        path: '',
        canActivate: [loggedInGuard],
        component: LayoutComponent,
        children: [
            { path: '', redirectTo: 'home', pathMatch: 'full' },
            {
                path: 'home',
                loadComponent: () =>
                    import('./home/home.component').then(m => m.HomeComponent)
            },
            {
                path: 'example-form',
                loadComponent: () =>
                    import('./example-form/example-form.component').then(m => m.ExampleFormComponent),
                canActivate: [loggedInGuard]
            },
            {
                path: 'example-table',
                loadComponent: () =>
                    import('./example-table/example-table.component').then(m => m.ExampleTableComponent),
                canActivate: [loggedInGuard]
            },
            {
                path: 'example-dialogs',
                loadComponent: () =>
                    import('./example-dialogs/example-dialogs.component').then(m => m.ExampleDialogsComponent),
                canActivate: [loggedInGuard]
            },
            {
                path: 'example-websockets',
                loadComponent: () =>
                    import('./example-websocket/example-websocket.component').then(m => m.ExampleWebsocketComponent),
                canActivate: [loggedInGuard]
            },
        ]
    },
    {
        path: 'login',
        loadComponent: () =>
            import('./login/login.component').then(m => m.LoginComponent),
        canActivate: [notLoggedInGuard]
    }
];

