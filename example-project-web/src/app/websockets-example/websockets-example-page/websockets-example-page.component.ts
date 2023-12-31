import {Component, OnInit} from '@angular/core';
import {UserWebsocketsService} from '../../shared/services/user-websockets.service';
import {WebsocketEvent} from '../../shared/interfaces/websockets/websocket-event';
import {BlocksApiService} from '../../shared/apis/blocks-api.service';
import {BreadcrumbsService} from '../../shared/components/breadcrumbs/breadcrumbs.service';
import {BasePageComponent} from '../../shared/components/base-page-component';

@Component({
  selector: 'app-websockets-example-page',
  templateUrl: './websockets-example-page.component.html',
  styleUrls: ['./websockets-example-page.component.scss']
})
export class WebsocketsExamplePageComponent extends BasePageComponent implements OnInit {
  events: string[] = [];

  constructor(private userWebsocketsService: UserWebsocketsService,
              private blocksApiService: BlocksApiService,
              private breadcrumbsService: BreadcrumbsService) {
    super();
    this.breadcrumbs = this.breadcrumbsService.getSimpleBreadcrumbs('Websockets Example');
  }

  ngOnInit(): void {
    this.addWsSubscriptions();
  }

  async addWsSubscriptions() {
    await this.userWebsocketsService.finishedConnecting();
    this.subscriptions.push(await this.userWebsocketsService.websocketGroupSubscribe('room', {'room_id': 1},
      (data: WebsocketEvent) => {
        this.events.push(`Room 1: ${data.payload['message']}`);
      }));
    this.subscriptions.push(await this.userWebsocketsService.websocketGroupSubscribe('room', {'room_id': 2},
      (data: WebsocketEvent) => {
        this.events.push(`Room 2: ${data.payload['message']}`);
      }));
  }

  async triggerEventA() {
    await this.blocksApiService.sendBlockEvent(1);
  }

  async triggerEventB() {
    await this.blocksApiService.sendBlockEvent(2);
  }
}
