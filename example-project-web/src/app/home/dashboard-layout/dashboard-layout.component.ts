import { Component } from '@angular/core';
import {AuthenticationService} from '../../shared/authentication/authentication.service';
import {RoutingService} from '../../shared/services/routing.service';

@Component({
  selector: 'app-dashboard-layout',
  templateUrl: './dashboard-layout.component.html',
  styleUrls: ['./dashboard-layout.component.scss']
})
export class DashboardLayoutComponent {

  constructor(public authService: AuthenticationService, public routingService: RoutingService) {
  }

  async logout(): Promise<void> {
    await this.authService.logout();
    this.routingService.navigateToLogin();
  }
}
