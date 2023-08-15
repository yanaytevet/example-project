import {Injectable} from '@angular/core';
import * as moment from 'moment';
import {Moment} from 'moment';

@Injectable({
  providedIn: 'root'
})
export class TimeUtilsService {
  DEFAULT_FORMAT = 'YYYY-MM-DDTHH:mm:ss.SSSSSSZZ';

  constructor() {
  }

  public now(): Moment {
    return moment();
  }

  public getDiffMinutes(startMoment: Moment, endMoment: Moment): number {
    return moment.duration(endMoment.diff(startMoment)).asMinutes();
  }

  public getDiffMinutesFromNow(startMoment: Moment): number {
    return this.getDiffMinutes(startMoment, this.now());
  }

  public momentToDefaultStr(momentObj: Moment): string {
    return moment(momentObj).utc().format(this.DEFAULT_FORMAT);
  }

  public defaultStrToMoment(dateStr: string): Moment {
    return moment(dateStr);
  }


}
