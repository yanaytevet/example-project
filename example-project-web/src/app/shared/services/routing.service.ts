import { Injectable, inject } from '@angular/core';
import { Router, UrlTree } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RoutingService {
  private router = inject(Router);

  // Root route
  getRootUrl(): UrlTree {
    return this.router.createUrlTree(['/']);
  }

  navigateToRoot(): Promise<boolean> {
    return this.router.navigateByUrl(this.getRootUrl());
  }

  // Home route
  getHomeUrl(): UrlTree {
    return this.router.createUrlTree(['/home']);
  }

  navigateToHome(): Promise<boolean> {
    return this.router.navigateByUrl(this.getHomeUrl());
  }

  // Login route
  getLoginUrl(): UrlTree {
    return this.router.createUrlTree(['/login']);
  }

  navigateToLogin(): Promise<boolean> {
    return this.router.navigateByUrl(this.getLoginUrl());
  }

  // Example Form route
  getExampleFormUrl(): UrlTree {
    return this.router.createUrlTree(['/example-form']);
  }

  navigateToExampleForm(): Promise<boolean> {
    return this.router.navigateByUrl(this.getExampleFormUrl());
  }

  // Example Table route
  getExampleTableUrl(): UrlTree {
    return this.router.createUrlTree(['/example-table']);
  }

  navigateToExampleTable(): Promise<boolean> {
    return this.router.navigateByUrl(this.getExampleTableUrl());
  }

  // Example Dialogs route
  getExampleDialogsUrl(): UrlTree {
    return this.router.createUrlTree(['/example-dialogs']);
  }

  navigateToExampleDialogs(): Promise<boolean> {
    return this.router.navigate(['/example-dialogs']);
  }

  // Example Websockets route
  getExampleWebsocketsUrl(): UrlTree {
    return this.router.createUrlTree(['/example-websockets']);
  }

  navigateToExampleWebsockets(): Promise<boolean> {
    return this.router.navigate(['/example-websockets']);
  }
}
