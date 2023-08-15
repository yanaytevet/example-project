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

  navigateToLogin(redirectUrl?: string): void {
    this.router.navigate(this.getLoginUrl(), { queryParams: { redirectUrl } });
  }

  // Home

  getHomeUrl(): any[] {
    return ['/'];
  }

  navigateToRoot(): void {
    this.router.navigate(['/']);
  }

  async navigateToRootAndRefresh(): Promise<void> {
    await this.router.navigate(['/']);
    this.forceRefresh();
  }
}
