import {Injectable} from '@angular/core';
import {Subject, Subscription} from "rxjs";
import * as humps from "humps";
import {WebsocketEvent, ZWebsocketEvent} from '../interfaces/websockets/websocket-event';

@Injectable({
  providedIn: 'root'
})

export class UserWebsocketsService {
  private readonly _websocketListener = new Subject<WebsocketEvent>();
  readonly websocketListener$ = this._websocketListener.asObservable();

  constructor() {}

  public async connect() {
    // sleep for 1 second to allow the server to start
    await new Promise(resolve => setTimeout(resolve, 1000));
    const protocol = window.location.host.includes('localhost') ? 'ws' : 'wss';
    const url = `${protocol}://${window.location.host.includes('localhost') ? 'localhost:8000' : window.location.host}/ws/socket/`;
    let ws = new WebSocket(url);
    ws.onmessage = (event) => {
      const camelizedEvent = humps.camelizeKeys(JSON.parse(event.data));
      ZWebsocketEvent.parse(camelizedEvent);
      this._websocketListener.next(camelizedEvent);
    }
  }


  public websocketSubscribe(eventType: string, callback: (data: WebsocketEvent) => void): Subscription {
    return this.websocketListener$.subscribe((data: WebsocketEvent) => {
      if (data && data.eventType === eventType) {
        callback(data);
      }
    });
  }

}
