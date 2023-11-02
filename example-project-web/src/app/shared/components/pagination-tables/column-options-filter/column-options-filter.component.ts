import {Component, Input} from '@angular/core';
import {PaginationDataHandler} from "../pagination-data-handler";
import {Option} from '../../../interfaces/util/option';

@Component({
  selector: 'app-column-options-filter',
  templateUrl: './column-options-filter.component.html',
  styleUrls: ['./column-options-filter.component.scss']
})

export class ColumnOptionsFilterComponent {
  @Input() options: Option[];
  @Input() paginationDataHandler: PaginationDataHandler<any>;
  @Input() filterKey: string;
  @Input() showSearch = true;
  filteredOptions: Option[];
  filterValue: string;
  checkedValues: Map<string, boolean>;

  constructor() {
    this.filteredOptions = [];
    this.filterValue = '';
    this.checkedValues = new Map<string, boolean>();
  }

  ngOnInit() {
    this.filterValues();
  }

  filterValues() {
    this.filteredOptions = this.options.filter(option =>
      option.display.toLowerCase().includes(this.filterValue.toLowerCase())
    );
  }

  onCheckboxChange(value: string) {
    if (this.checkedValues.get(value)) {
      this.checkedValues.set(value, false)
    }
    else {
      this.checkedValues.set(value, true)
    }
    const values = Array.from(this.checkedValues).filter(([key, value]) => value === true).map(([key, value]) => key);
    const filter_key = `${this.filterKey}__in`
    if (values.length > 0) {
      this.paginationDataHandler.setFilter(filter_key, values);
    } else {
      this.paginationDataHandler.clearFilter(filter_key)
    }
  }
}
