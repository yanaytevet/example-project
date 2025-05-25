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

  public getSimpleBreadcrumbs(text: string): LinkItem[] {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
      {text, linkArr: [], active: false},
    ];
  }

  public getBattlefieldsBreadcrumbs(name: string) {
    return [
      {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
      {text: 'Battlefields', linkArr: this.routingService.getBattlefieldsTablePageUrl(), active: true},
      {text: name, linkArr: [], active: false},
    ];
  }
}
