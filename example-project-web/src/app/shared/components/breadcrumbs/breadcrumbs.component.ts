import {Component, input} from '@angular/core';
import {LinkItem} from './link-item';
import {RouterLink} from '@angular/router';
import {NgIcon, provideIcons} from '@ng-icons/core';
import {bootstrapChevronRight} from '@ng-icons/bootstrap-icons';

@Component({
    selector: 'app-breadcrumbs',
    templateUrl: './breadcrumbs.component.html',
    imports: [
        RouterLink,
        NgIcon,
    ],
    providers: [
        provideIcons({ bootstrapChevronRight })
    ]
})
export class BreadcrumbsComponent {
  linkItems = input<LinkItem[]>();
  mode = input<'white' | 'black'>('black');
}
