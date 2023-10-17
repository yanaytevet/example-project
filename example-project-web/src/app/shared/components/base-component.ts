import {Subscription} from 'rxjs';
import {Component, OnDestroy} from '@angular/core';
import {LinkItem} from './breadcrumbs/link-item';
@Component({
  template: ''
})
export class BaseComponent implements OnDestroy {
  protected subscriptions: Subscription[] = [];

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }
}
