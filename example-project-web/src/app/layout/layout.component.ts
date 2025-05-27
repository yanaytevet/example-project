import {Component, inject} from '@angular/core';
import {RouterLink, RouterOutlet} from '@angular/router';
import {AuthenticationService} from '../shared/authentication/authentication.service';
import {RoutingService} from '../shared/services/routing.service';
import {provideIcons} from '@ng-icons/core';
import {bootstrapBoxArrowRight, bootstrapChevronDown} from '@ng-icons/bootstrap-icons';
import {MenuButtonComponent} from '../shared/components/menu-button/menu-button.component';
import {Action} from '../shared/interfaces/util/action';

@Component({
  selector: 'app-layout',
  imports: [
    RouterLink,
    RouterOutlet,
    MenuButtonComponent,
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.css'
})
export class LayoutComponent {
  public authService = inject(AuthenticationService);
  public routingService = inject(RoutingService);

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
}
