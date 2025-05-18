import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {HTTP_INTERCEPTORS, provideHttpClient, withInterceptorsFromDi} from '@angular/common/http';
import {LoggedInGuard} from './shared/authentication/logged-in-guard.service';
import {LoggedOutGuard} from './shared/authentication/logged-out-guard.service';
import {AdminGuard} from './shared/authentication/admin-guard.service';
import {ErrorHandlingInterceptor} from './shared/interceptors/error-handling-interceptor';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {RouterModule} from '@angular/router';
import {CommonModule} from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HomeModule} from './home/home.module';
import {NgxPermissionsModule} from 'ngx-permissions';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {SharedModule} from './shared/shared.module';

@NgModule({ declarations: [
        AppComponent
    ],
    bootstrap: [AppComponent], imports: [CommonModule,
        BrowserModule,
        FormsModule,
        ReactiveFormsModule,
        RouterModule,
        NgxPermissionsModule.forRoot(),
        MatSnackBarModule,
        SharedModule,
        HomeModule,
        AppRoutingModule,
        BrowserAnimationsModule], providers: [
        {
            provide: HTTP_INTERCEPTORS,
            useClass: ErrorHandlingInterceptor,
            multi: true,
        },
        LoggedInGuard,
        LoggedOutGuard,
        AdminGuard,
        provideHttpClient(withInterceptorsFromDi())
    ] })
export class AppModule { }
