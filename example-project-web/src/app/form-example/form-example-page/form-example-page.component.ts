import {Component} from '@angular/core';
import {InputDebounce} from '../../shared/inputs/input-debounce';
import {debounce} from 'rxjs';
import {BaseComponent} from '../../shared/components/base-component';
import {BreadcrumbsService} from '../../shared/components/breadcrumbs/breadcrumbs.service';
import {Option} from '../../shared/interfaces/util/option';

@Component({
  selector: 'app-form-example-page',
  templateUrl: './form-example-page.component.html',
  styleUrls: ['./form-example-page.component.scss']
})
export class FormExamplePageComponent extends BaseComponent {
  canEdit = true;
  inputDebounce = new InputDebounce<string>();
  textAreaDebounce = new InputDebounce<string>();
  values: string[] = [];
  options: Option[] = [
    {value: 'test1', display: 'Test 1'},
    {value: 'test2', display: 'Test 2'},
    {value: 'test3', display: 'Test 3'},
  ];

  constructor(private breadcrumbsService: BreadcrumbsService) {
    super();
    this.breadcrumbs = this.breadcrumbsService.getSimpleBreadcrumbs('Forms Example');
    this.inputDebounce.setValueWithoutTrigger('test');
    this.inputDebounce.valueChangedFinished$.subscribe(value => {
      this.values.push(value);
    });
    this.textAreaDebounce.valueChangedFinished$.subscribe(value => {
      this.values.push(value);
    });
  }

  chipsValuesChanged(chipsValues: string[]) {
    this.values.push(JSON.stringify(chipsValues));
  }

  chipsAutocompleteValuesChanged(optionsList: Option[]) {
    this.values.push(JSON.stringify(optionsList));
  }

  updateDisabled() {
    if (this.canEdit) {
      this.inputDebounce.ctrl.enable({emitEvent: false});
      this.textAreaDebounce.ctrl.enable({emitEvent: false});
    } else {
      this.inputDebounce.ctrl.disable({emitEvent: false});
      this.textAreaDebounce.ctrl.disable({emitEvent: false});
    }
  }
}
