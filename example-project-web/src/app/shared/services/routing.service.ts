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

  // Room

  getRoomByPlayerUrl(roomId: number): any[] {
    return ['/room', roomId, 'player'];
  }

  navigateToRoomByPlayer(roomId: number): void {
    this.router.navigate(this.getRoomByPlayerUrl(roomId));
  }

  getAlternativeRoomByPlayerUrl(roomId: number): any[] {
    return ['/room', roomId, 'alternative-player'];
  }

  navigateToAlternativeRoomByPlayer(roomId: number): void {
    this.router.navigate(this.getAlternativeRoomByPlayerUrl(roomId));
  }

  getRoomByGameMasterUrl(roomId: number): any[] {
    return ['/room', roomId, 'game-master'];
  }

  navigateToRoomByGameMaster(roomId: number): void {
    this.router.navigate(this.getRoomByGameMasterUrl(roomId));
  }
}
