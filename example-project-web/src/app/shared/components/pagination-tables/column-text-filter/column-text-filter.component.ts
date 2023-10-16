import {Component, Input} from '@angular/core';
import {PaginationDataHandler} from "../pagination-data-handler";
import {InputDebounce} from '../../../inputs/input-debounce';
import {BaseComponent} from '../../base-component';

@Component({
  selector: 'app-column-text-filter',
  templateUrl: './column-text-filter.component.html',
  styleUrls: ['./column-text-filter.component.scss']
})

export class ColumnTextFilterComponent extends BaseComponent {
  @Input() paginationDataHandler: PaginationDataHandler<any>;
  @Input() filterKey: string;
  filterDebounce = new InputDebounce('');

  constructor() {
    super();
  }

  ngOnInit() {
    this.subscriptions.push(this.filterDebounce.valueChangedFinished$.subscribe(value => {
      const filterStr = `${this.filterKey}__contains`
      if (value.length > 0) {
        this.paginationDataHandler.setFilter(filterStr, value);
      } else {
        this.paginationDataHandler.clearFilter(filterStr)
      }
    }));
  }
}
