import {Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {Option} from '../../../interfaces/util/option';
import {FormControl} from '@angular/forms';
import {CdkDragDrop, moveItemInArray} from '@angular/cdk/drag-drop';
import {MatAutocompleteSelectedEvent} from '@angular/material/autocomplete';
import {BaseComponent} from '../../base-component';


@Component({
  selector: 'app-chips-autocomplete-drag',
  templateUrl: './chips-autocomplete-drag.component.html',
  styleUrls: ['./chips-autocomplete-drag.component.scss']
})
export class ChipsAutocompleteDragComponent extends BaseComponent implements OnInit {
  valueToOption: Record<string, Option> = {};

  _options: Option[] = [];
  @Input() set options(val: Option[]) {
    this._options = val;
    val.forEach((option) => {
      this.valueToOption[option.value] = option;
    });
    this.updateFilteredOptions();
  }

  get options(): Option[] {
    return this._options;
  }

  _values: any[] = [];
  @Input() set values(val: any[]) {
    this._values = val;
  }
  get values(): any[] {
    return this._values;
  }

  @Input() label: string = '';

  _canEdit: boolean = false;
  @Input() set canEdit(val: boolean) {
    this._canEdit = val;
    if (val) {
      this.filterCtrl.enable();
    } else {
      this.filterCtrl.disable();
    }
  }
  get canEdit(): boolean {
    return this._canEdit;
  }
  filterCtrl = new FormControl('');
  filteredOptions: Option[];

  @ViewChild('filterInput') fruitInput: ElementRef<HTMLInputElement>;

  @Output() valuesChange = new EventEmitter<any[]>();

  constructor() {
    super();
  }

  ngOnInit(): void {
    this.subscriptions.push(this.filterCtrl.valueChanges.subscribe((value) => {
      this.updateFilteredOptions();
    }));
    this.updateFilteredOptions();
  }

  updateFilteredOptions(): void {
    const filterValue = this.filterCtrl.value;
    if (typeof filterValue !== 'string') {
      return
    }
    const filterValueLower = filterValue ? filterValue.toLowerCase() : '';
    this.filteredOptions = this.options.filter(option => {
      if (filterValueLower.length) {
        if (!option.display.toLowerCase().includes(filterValueLower)) {
          return false;
        }
      }
      if (this.values.find((val) => val === option.value)) {
        return false;
      }
      return true;
    });
  }

  remove(valueToRemove: any): void {
    if (!this.canEdit) {
      return;
    }
    const index = this.values.indexOf(valueToRemove);

    if (index >= 0) {
      this.values.splice(index, 1);
      this.valuesChange.emit(this.values);
    }

    this.updateFilteredOptions();
  }

  selected(event: MatAutocompleteSelectedEvent): void {
    if (!this.canEdit) {
      return;
    }
    this.values.push(event.option.value.value);
    this.valuesChange.emit(this.values);
    this.fruitInput.nativeElement.value = '';
    this.filterCtrl.setValue('');
  }

  drop(event: CdkDragDrop<Option[]>) {
    if (!this.canEdit) {
      return;
    }
    moveItemInArray(this.values, event.previousIndex, event.currentIndex);
    this.valuesChange.emit(this.values);
  }
}
