import {Component, inject} from '@angular/core';
import {RoutingService} from '../shared/services/routing.service';
import {NgIcon, provideIcons} from '@ng-icons/core';
import {bootstrapChatSquare, bootstrapFileEarmark, bootstrapLightning, bootstrapTable} from '@ng-icons/bootstrap-icons';

@Component({
  selector: 'app-home',
  imports: [NgIcon],
  providers: [provideIcons({
    bootstrapFileEarmark, bootstrapTable, bootstrapChatSquare, bootstrapLightning
  })],
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
