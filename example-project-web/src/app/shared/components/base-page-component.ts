import {Component} from '@angular/core';
import {LinkItem} from './breadcrumbs/link-item';
import {BaseComponent} from './base-component';

@Component({
  template: ''
})
export class BasePageComponent extends BaseComponent {
  protected breadcrumbs: LinkItem[] = [];
}
