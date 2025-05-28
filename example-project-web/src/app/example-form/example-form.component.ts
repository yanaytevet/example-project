import {Component, effect, inject} from '@angular/core';
import {Option} from '../shared/interfaces/util/option';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {BasePageComponent} from '../shared/components/base-page-component';
import {InputDebounce} from '../shared/data/input-debouncer';
import {BreadcrumbsComponent} from '../shared/components/breadcrumbs/breadcrumbs.component';
import {BreadcrumbsService} from '../shared/components/breadcrumbs/breadcrumbs.service';
import {LinkItem} from '../shared/components/breadcrumbs/link-item';

@Component({
  selector: 'app-example-form',
  imports: [FormsModule, ReactiveFormsModule, CommonModule, BreadcrumbsComponent],
  templateUrl: './example-form.component.html',
  styleUrl: './example-form.component.css'
})
export class ExampleFormComponent extends BasePageComponent{
  breadcrumbsService = inject(BreadcrumbsService);

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
    this.breadcrumbs = this.breadcrumbsService.getExampleFormBreadcrumbs();

    this.subscriptions.push(this.inputDebouncer.valueChangedFinished$.subscribe(newVal => {
      this.values.push(newVal);
    }));

    this.subscriptions.push(this.textAreaDebouncer.valueChangedFinished$.subscribe(newVal => {
      this.values.push(newVal);
    }));
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
