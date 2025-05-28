import {Component, inject} from '@angular/core';
import {RoutingService} from '../shared/services/routing.service';
import {NgIcon, provideIcons} from '@ng-icons/core';
import {bootstrapChatSquare, bootstrapFileEarmark, bootstrapLightning, bootstrapTable} from '@ng-icons/bootstrap-icons';
import {BreadcrumbsComponent} from '../shared/components/breadcrumbs/breadcrumbs.component';
import {BreadcrumbsService} from '../shared/components/breadcrumbs/breadcrumbs.service';
import {BasePageComponent} from '../shared/components/base-page-component';

@Component({
  selector: 'app-home',
  imports: [NgIcon, BreadcrumbsComponent],
  providers: [provideIcons({
    bootstrapFileEarmark, bootstrapTable, bootstrapChatSquare, bootstrapLightning
  })],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent extends BasePageComponent{
  routingService = inject(RoutingService);
  breadcrumbsService = inject(BreadcrumbsService);

  constructor() {
    super();
    this.breadcrumbs = this.breadcrumbsService.getHomeBreadcrumbs();
  }

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
