import {Injectable} from '@angular/core';
import {ActivationEnd, Router} from '@angular/router';
import * as moment from 'moment';
import {BaseApiService} from './base-api.service';


@Injectable({
  providedIn: 'root'
})
export class EventsAnalyticsService {
  startTimeStr: string = null;

  constructor(private router: Router, private baseApi: BaseApiService) {
    this.startTimeStr = moment().format('YYYYMMDDHHmmssSSS');
  }

  public registerRouter(): void {
    this.router.events.subscribe(event => {
      if (!(event instanceof ActivationEnd)) {
        return
      }
      if (!('snapshot' in event)) {
        return
      }
      if (!('data' in event.snapshot)) {
        return
      }
      if (!('routeName' in event.snapshot.data)) {
        return
      }
      this.sendEvent(`visit_page_${event.snapshot.data['routeName']}`, {});
    });
  }

  public async sendEvent(name: string, attributes: object): Promise<void> {
    const tabID = this.startTimeStr;
    await this.baseApi.post<void>(null, '/api/user-events/', {
        'name': name,
        'tab_id': tabID,
        'attributes': attributes
      }
    );
  }
}
