import {Component, effect} from '@angular/core';
import {Option} from '../shared/interfaces/util/option';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {BasePageComponent} from '../shared/components/base-page-component';
import {InputDebounce} from '../shared/data/input-debouncer';

@Component({
  selector: 'app-example-form',
  imports: [FormsModule, ReactiveFormsModule, CommonModule],
  templateUrl: './example-form.component.html',
  styleUrl: './example-form.component.css'
})
export class ExampleFormComponent extends BasePageComponent{
  canEdit = true;
  inputDebouncer = new InputDebounce<string>();
  textAreaDebouncer = new InputDebounce<string>();
  values: string[] = [];
  options: Option[] = [
    {value: 'test1', display: 'Test 1'},
    {value: 'test2', display: 'Test 2'},
    {value: 'test3', display: 'Test 3'},
  ];

  constructor() {
    super();
    this.inputDebouncer.setValueWithoutTrigger('test');
    this.updateDisabled(); // Set initial state of form controls

    this.subscriptions.push(this.inputDebouncer.valueChangedFinished$.subscribe(newVal => {
      this.values.push(newVal);
    }));

    this.subscriptions.push(this.textAreaDebouncer.valueChangedFinished$.subscribe(newVal => {
      this.values.push(newVal);
    }));
  }

  chipsValuesChanged(chipsValues: string[]) {
    this.values.push(JSON.stringify(chipsValues));
  }

  chipsAutocompleteValuesChanged(optionsList: Option[]) {
    this.values.push(JSON.stringify(optionsList));
  }

  updateDisabled() {
    if (this.canEdit) {
      this.inputDebouncer.ctrl.enable({emitEvent: false});
      this.textAreaDebouncer.ctrl.enable({emitEvent: false});
    } else {
      this.inputDebouncer.ctrl.disable({emitEvent: false});
      this.textAreaDebouncer.ctrl.disable({emitEvent: false});
    }
  }
}
