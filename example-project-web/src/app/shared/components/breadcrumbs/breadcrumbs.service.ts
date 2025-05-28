import {Injectable} from '@angular/core';
import {RoutingService} from '../../services/routing.service';
import {LinkItem} from './link-item';

@Injectable({
  providedIn: 'root'
})
export class BreadcrumbsService {

  constructor(private routingService: RoutingService) {
  }

  public getHomeBreadcrumbs(): LinkItem[] {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
    ];
  }

  public getExampleFormBreadcrumbs(): LinkItem[] {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
      {text: 'Example Form', linkArr: this.routingService.getExampleFormUrl(), active: true},
    ];
  }

  public getExampleTableBreadcrumbs(): LinkItem[] {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
      {text: 'Example Table', linkArr: this.routingService.getExampleTableUrl(), active: true},
    ];
  }

  public getExampleDialogsBreadcrumbs(): LinkItem[] {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
      {text: 'Example Dialogs', linkArr: this.routingService.getExampleDialogsUrl(), active: true},
    ];
  }

  public getExampleWebsocketsBreadcrumbs(): LinkItem[] {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
      {text: 'Example Websockets', linkArr: this.routingService.getExampleWebsocketsUrl(), active: true},
    ];
  }
}
