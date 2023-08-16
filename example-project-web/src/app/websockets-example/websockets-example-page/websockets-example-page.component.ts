import {Component, OnInit} from '@angular/core';
import {UserWebsocketsService} from '../../shared/services/user-websockets.service';
import {WebsocketEvent} from '../../shared/interfaces/websockets/websocket-event';
import {BlocksApiService} from '../../shared/apis/blocks-api.service';
import {BaseComponent} from '../../shared/components/base-component';

@Component({
  selector: 'app-websockets-example-page',
  templateUrl: './websockets-example-page.component.html',
  styleUrls: ['./websockets-example-page.component.scss']
})
export class WebsocketsExamplePageComponent extends BaseComponent implements OnInit {
  events: string[] = [];

  constructor(private userWebsocketsService: UserWebsocketsService,
              private blocksApiService: BlocksApiService) {
    super();
  }

  ngOnInit(): void {
    this.subscriptions.push(this.userWebsocketsService.websocketSubscribe('actionTypeA',
      (data: WebsocketEvent) => {
        this.events.push(`event A: ${data.payload['message']}`);
      }));
    this.subscriptions.push(this.userWebsocketsService.websocketSubscribe('actionTypeB',
      (data: WebsocketEvent) => {
        this.events.push(`event B: ${data.payload['message']}`);
      }));
  }

  async triggerEventA() {
    await this.blocksApiService.sendBlockEvent('actionTypeA');
  }

  async triggerEventB() {
    await this.blocksApiService.sendBlockEvent('actionTypeB');
  }
}
