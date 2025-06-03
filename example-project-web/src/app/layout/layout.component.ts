import {Component, inject} from '@angular/core';
import {RouterLink, RouterOutlet} from '@angular/router';
import {AuthenticationService} from '../shared/authentication/authentication.service';
import {RoutingService} from '../shared/services/routing.service';
import {
  bootstrapBoxArrowRight,
  bootstrapChevronDown,
  bootstrapMoonFill,
  bootstrapSunFill
} from '@ng-icons/bootstrap-icons';
import {MenuButtonComponent} from '../shared/components/menu-button/menu-button.component';
import {Action} from '../shared/interfaces/util/action';
import {DarkModeService} from '../shared/services/dark-mode.service';
import {NgIcon} from '@ng-icons/core';

@Component({
  selector: 'app-layout',
  imports: [
    RouterLink,
    RouterOutlet,
    MenuButtonComponent,
    NgIcon,
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.css'
})
export class LayoutComponent {
  public authService = inject(AuthenticationService);
  public routingService = inject(RoutingService);
  public darkModeService = inject(DarkModeService);

  userMenuActions: Action[] = [
    {
      display: 'Logout',
      icon: bootstrapBoxArrowRight,
      callback: () => this.logout()
    }
  ];

  async logout() {
    await this.authService.logout();
  }

  protected readonly bootstrapChevronDown = bootstrapChevronDown;
  protected readonly bootstrapMoonFill = bootstrapMoonFill;
  protected readonly bootstrapSunFill = bootstrapSunFill;
}
