import {Component} from '@angular/core';
import {InputDebounce} from '../../shared/inputs/input-debounce';
import {debounce} from 'rxjs';

@Component({
  selector: 'app-form-example-page',
  templateUrl: './form-example-page.component.html',
  styleUrls: ['./form-example-page.component.scss']
})
export class FormExamplePageComponent {
  inputDebounce = new InputDebounce<string>();
  values: string[] = [];

  constructor() {
    this.inputDebounce.setValueWithoutTrigger('test');
    this.inputDebounce.valueChangedFinished$.subscribe(value => {
      this.values.push(value);
    });
  }

  protected readonly debounce = debounce;
}
