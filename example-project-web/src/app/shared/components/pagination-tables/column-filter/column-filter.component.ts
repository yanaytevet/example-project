import {Component, Input} from '@angular/core';
import {PaginationDataHandler} from "../pagination-data-handler";

@Component({
  selector: 'app-column-filter',
  templateUrl: './column-filter.component.html',
  styleUrls: ['./column-filter.component.scss']
})

export class ColumnFilterComponent {
  @Input() values: string[];
  @Input() genericDataHandler: PaginationDataHandler<any>;
  @Input() filterKey: string;
  filteredValues: string[];
  filterValue: string;
  checkedValues: Map<string, boolean>;

  constructor() {
    this.filteredValues = [];
    this.filterValue = '';
    this.checkedValues = new Map<string, boolean>();
  }

  ngOnInit() {
    this.filterValues();
  }

  filterValues() {
    this.filteredValues = this.values.filter(value =>
      value.toLowerCase().startsWith(this.filterValue.toLowerCase())
    );
  }

  onCheckboxChange(value: string) {
    if (this.checkedValues.get(value)) {
      this.checkedValues.set(value, false)
    }
    else {
      this.checkedValues.set(value, true)
    }
    this.genericDataHandler.setFilter(this.filterKey,
      Array.from(this.checkedValues).filter(([key, value]) => value === true).map(([key, value]) => key));
  }
}
