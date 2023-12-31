import { Injectable } from '@angular/core';
import {Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class RoutingService {

  constructor(private router: Router) {
  }

  forceRefresh(): void {
    location.reload();
  }

  // Login

  getLoginUrl(): any[] {
    return ['/login'];
  }

  async navigateToLogin(redirectUrl?: string): Promise<void> {
    await this.router.navigate(this.getLoginUrl(), { queryParams: { redirectUrl } });
  }

  // Home

  getHomeUrl(): any[] {
    return ['/'];
  }

  async navigateToRoot(): Promise<void> {
    await this.router.navigate(['/']);
  }

  async navigateToRootAndRefresh(): Promise<void> {
    await this.router.navigate(['/']);
    this.forceRefresh();
  }

  // Websockets Example

  getWebsocketsExamplePageUrl(): any[] {
    return ['/websockets-example'];
  }

  async navigateToWebsocketsExamplePage(): Promise<void> {
    await this.router.navigate(this.getWebsocketsExamplePageUrl());
  }

  // Dialog Example

  getDialogsExamplePageUrl(): any[] {
    return ['/dialogs-example'];
  }

  async navigateToDialogsExamplePage(): Promise<void> {
    await this.router.navigate(this.getDialogsExamplePageUrl());
  }

  // Forms Example

  getFormsExamplePageUrl(): any[] {
    return ['/form-example'];
  }

  async navigateToFormsExamplePage(): Promise<void> {
    await this.router.navigate(this.getFormsExamplePageUrl());
  }

  // Tables Example

  getTablesExamplePageUrl(): any[] {
    return ['/table-example'];
  }

  async navigateToTablesExamplePage(): Promise<void> {
    await this.router.navigate(this.getTablesExamplePageUrl());
  }
}
