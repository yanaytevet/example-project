import {Component, input, OnInit} from '@angular/core';
import {LinkItem} from './link-item';
import {NgClass} from '@angular/common';
import {RouterLink} from '@angular/router';
import {NgIcon, NgIconsModule, provideIcons} from '@ng-icons/core';
import {bootstrapChevronRight} from '@ng-icons/bootstrap-icons';

@Component({
    selector: 'app-breadcrumbs',
    templateUrl: './breadcrumbs.component.html',
    imports: [
        RouterLink,
        NgIconsModule,
        NgIcon,
    ],
    providers: [
        provideIcons({ bootstrapChevronRight })
    ]
})
export class BreadcrumbsComponent implements OnInit {
  linkItems = input<LinkItem[]>();
  mode = input<'white' | 'black'>('black');

  constructor() { }

  ngOnInit(): void {
  }

  get textClass() {
    return {
      'text-base': true,
      'leading-tight': true,
      'no-underline': true,
      'text-primary': true,
      'transition-all': true,
      'duration-300': true
    };
  }

  get iconClass() {
    return {
      'mx-2.5': true,
      'h-5': true,
      'w-5': true,
      'text-primary': true
    };
  }
}
