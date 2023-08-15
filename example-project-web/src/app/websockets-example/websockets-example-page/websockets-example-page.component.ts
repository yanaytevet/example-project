import {Component, OnDestroy, OnInit} from '@angular/core';
import {UserWebsocketsService} from '../../shared/services/user-websockets.service';
import {Subscription} from 'rxjs';
import {WebsocketEvent} from '../../shared/interfaces/websockets/websocket-event';
import {BlocksApiService} from '../../shared/apis/blocks-api.service';

@Component({
  selector: 'app-websockets-example-page',
  templateUrl: './websockets-example-page.component.html',
  styleUrls: ['./websockets-example-page.component.scss']
})
export class WebsocketsExamplePageComponent implements OnInit, OnDestroy {
  actionTypeASubscription: Subscription;
  actionTypeBSubscription: Subscription;

  events: string[] = [];

  constructor(private userWebsocketsService: UserWebsocketsService,
              private blocksApiService: BlocksApiService) {
  }

  ngOnInit(): void {
    this.actionTypeASubscription = this.userWebsocketsService.websocketSubscribe('actionTypeA',
      (data: WebsocketEvent) => {
        this.events.push(`event A: ${data.payload['message']}`);
      });
    this.actionTypeBSubscription = this.userWebsocketsService.websocketSubscribe('actionTypeB',
      (data: WebsocketEvent) => {
        this.events.push(`event B: ${data.payload['message']}`);
      });
  }

  ngOnDestroy(): void {
    this.actionTypeASubscription.unsubscribe();
    this.actionTypeBSubscription.unsubscribe();
  }

  async triggerEventA() {
    await this.blocksApiService.sendBlockEvent('actionTypeA');
  }

  async triggerEventB() {
    await this.blocksApiService.sendBlockEvent('actionTypeB');
  }
}
