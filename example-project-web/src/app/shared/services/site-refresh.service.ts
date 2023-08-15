import {Injectable} from '@angular/core';
import {Moment} from 'moment';
import {NavigationEnd, Router} from '@angular/router';
import {TimeUtilsService} from './time-utils.service';

@Injectable({
  providedIn: 'root'
})
export class SiteRefreshService {
  latestLoadMoment: Moment = null;
  readonly MINUTES_TO_REFRESH = 180;

  constructor(private router: Router, public timeUtilsService: TimeUtilsService) {
    this.latestLoadMoment = this.timeUtilsService.now();
  }

  public registerRouter(): void {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.checkReload();
      }
    });
  }

  checkReload(): void {
    if (this.timeUtilsService.getDiffMinutesFromNow(this.latestLoadMoment) >= this.MINUTES_TO_REFRESH) {
      location.reload();
    }
  }
}
