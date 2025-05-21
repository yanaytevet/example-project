import {Component, HostListener, inject} from '@angular/core';
import {RouterLink, RouterOutlet} from '@angular/router';
import {AuthenticationService} from '../shared/authentication/authentication.service';
import {RoutingService} from '../shared/services/routing.service';

@Component({
  selector: 'app-layout',
  imports: [
    RouterLink,
    RouterOutlet,
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.css'
})
export class LayoutComponent {
  isUserMenuOpen = false;
  public authService = inject(AuthenticationService);
  public routingService = inject(RoutingService);

  @HostListener('document:click', ['$event'])
  handleClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (this.isUserMenuOpen && !target.closest('.user-menu-container')) {
      this.isUserMenuOpen = false;
    }
  }

  toggleUserMenu(event: MouseEvent) {
    event.stopPropagation();
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  async logout() {
    await this.authService.logout();
    this.isUserMenuOpen = false;
  }
}
