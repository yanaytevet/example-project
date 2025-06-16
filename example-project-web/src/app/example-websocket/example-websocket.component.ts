import {Component, inject, OnInit} from '@angular/core';
import {BasePageComponent} from '../shared/components/base-page-component';
import {UserWebsocketsService} from '../shared/services/user-websockets.service';
import {WebsocketEvent} from '../shared/interfaces/websockets/websocket-event';
import {postSampleWebsocketView} from '../../generated-files/api/blocks';
import {CommonModule} from '@angular/common';
import {BreadcrumbsComponent} from '../shared/components/breadcrumbs/breadcrumbs.component';
import {BreadcrumbsService} from '../shared/components/breadcrumbs/breadcrumbs.service';

@Component({
  selector: 'app-example-websocket',
  imports: [CommonModule, BreadcrumbsComponent],
  templateUrl: './example-websocket.component.html',
  styleUrl: './example-websocket.component.css'
})
export class ExampleWebsocketComponent extends BasePageComponent implements OnInit {
  events: string[] = [];
  userWebsocketsService = inject(UserWebsocketsService);
  breadcrumbsService = inject(BreadcrumbsService);

  constructor() {
    super();
    this.breadcrumbs = this.breadcrumbsService.getExampleWebsocketsBreadcrumbs();
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
    await postSampleWebsocketView({body: {room_id: 1}});
  }

  async triggerEventB() {
    await postSampleWebsocketView({body: {room_id: 2}});
  }
}
