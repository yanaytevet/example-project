import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { RoutingService } from '../shared/services/routing.service';

@Component({
  selector: 'app-home',
  imports: [
    RouterLink
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  routingService = inject(RoutingService);

  navigateToExampleForm(): void {
    this.routingService.navigateToExampleForm();
  }

  navigateToExampleTable(): void {
    this.routingService.navigateToExampleTable();
  }

  navigateToExampleDialogs(): void {
    this.routingService.navigateToExampleDialogs();
  }

  navigateToExampleWebsockets(): void {
    this.routingService.navigateToExampleWebsockets();
  }
}
