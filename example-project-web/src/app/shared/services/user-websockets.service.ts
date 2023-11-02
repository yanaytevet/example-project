import {Injectable} from '@angular/core';
import {BehaviorSubject, Subject, Subscription} from "rxjs";
import * as humps from "humps";
import {WebsocketEvent, ZWebsocketEvent} from '../interfaces/websockets/websocket-event';
import {BaseApiService} from './base-api.service';
import {WebsocketGroupInfo, ZWebsocketGroupInfo} from '../interfaces/websockets/websocket-group-info';
import {StringUtilsService} from './string-utils.service';
import {AuthenticationService} from '../authentication/authentication.service';
import {AuthUser} from '../interfaces/users/auth-user';

@Injectable({
  providedIn: 'root'
})

export class UserWebsocketsService {
  TIMEOUT_MS = 30000;

  private ws: WebSocket = null;
  private readonly _websocketIsReady = new BehaviorSubject<boolean>(false);
  readonly websocketIsReady$ = this._websocketIsReady.asObservable();

  private readonly _websocketListener = new Subject<WebsocketEvent>();
  readonly websocketListener$ = this._websocketListener.asObservable();

  private readonly _websocketConnectedToGroupListener = new Subject<WebsocketEvent>();
  readonly websocketConnectedToGroupListener$ = this._websocketConnectedToGroupListener.asObservable();

  constructor(private stringUtils: StringUtilsService, private authService: AuthenticationService) {
    this.authService.authUser$.subscribe(async (authUser: AuthUser) => {
      if (authUser) {
        await this.disconnect();
        await this.connect();
      }
    });
  }

  public async connect() {
    // sleep for 1 second to allow the server to start
    await new Promise(resolve => setTimeout(resolve, 1000));
    const usesSsl = location.protocol === "https:";
    const protocol = usesSsl ? 'wss' : 'ws';
    const url = `${protocol}://${usesSsl ? window.location.host : 'localhost:8000'}/ws/socket/`;
    this.ws = new WebSocket(url);
    this.ws.onmessage = (event) => {
      const camelizedEvent: WebsocketEvent = humps.camelizeKeys(JSON.parse(event.data));
      ZWebsocketEvent.parse(camelizedEvent);
      if (camelizedEvent.isConnectionEvent) {
        this._websocketConnectedToGroupListener.next(camelizedEvent);
      } else {
        this._websocketListener.next(camelizedEvent);
      }
    }
    this.ws.onopen = () => {
      this._websocketIsReady.next(true);
    };
  }

  public async disconnect() {
    if (!this.ws) {
      return;
    }
    this._websocketIsReady.next(false);
    this.ws.close();
  }

  public async finishedConnecting() {
    await new Promise(resolve => {
      this.websocketIsReady$.subscribe((isReady: boolean) => {
        if (isReady) {
          resolve(null);
        }
      });
    });
  }


  public async websocketGroupSubscribe(eventType: string, additionalInfo: object, callback: (data: WebsocketEvent) => void): Promise<Subscription> {
    let groupInfo: WebsocketEvent = null;
    const actionHash = this.stringUtils.generateRandomString(32);
    const succeed = await new Promise(resolve => {
      setTimeout(() => {
        resolve(false);
      }, this.TIMEOUT_MS);
      this.websocketConnectedToGroupListener$.subscribe((data: WebsocketEvent) => {
        if (data && data.actionHash === actionHash) {
          groupInfo = data;
          resolve(true);
        }
      });
      this.ws.send(JSON.stringify({
        'action': 'subscribe',
        'action_hash': actionHash,
        'event_type': eventType,
        'additional_info': additionalInfo,
      }));
    });
    return this.websocketListener$.subscribe((data: WebsocketEvent) => {
      if (data && data.groupName === groupInfo.groupName) {
        callback(data);
      }
    });
  }

}
