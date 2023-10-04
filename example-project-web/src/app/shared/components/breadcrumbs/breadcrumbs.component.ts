import {Component, Input, OnInit} from '@angular/core';
import {LinkItem} from './link-item';

@Component({
  selector: 'app-breadcrumbs',
  templateUrl: './breadcrumbs.component.html',
  styleUrls: ['./breadcrumbs.component.scss']
})
export class BreadcrumbsComponent implements OnInit {
  @Input() linkItems: LinkItem[];
  @Input() mode: 'white' | 'black' = 'black';

  constructor() { }

  ngOnInit(): void {
  }

}
