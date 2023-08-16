import {debounceTime, distinctUntilChanged} from 'rxjs/operators';
import {Observable, Subject} from 'rxjs';
import {FormControl} from '@angular/forms';

export class InputDebounce<T> {
  valueChangedSub: Subject<T> = new Subject<T>();
  valueChangedFinishedSub: Subject<T> = new Subject<T>();
  valueChangedFinished$: Observable<T> = this.valueChangedFinishedSub.asObservable();
  value: T = null;
  ctrl = new FormControl<T>(null);

  constructor(initValue?: T) {
    this.valueChangedSub.pipe(
      debounceTime(1000),
      distinctUntilChanged())
      .subscribe( newValue => {
        this.value = newValue;
        this.valueChangedFinishedSub.next(newValue);
      });

    this.ctrl.valueChanges.subscribe(event => {
      this.onValueChangedInCtrl(event);
    });

    if (initValue !== undefined) {
      this.setValue(initValue);
    }
  }

  onValueChangedInCtrl(newValue: T): void {
    this.valueChangedSub.next(newValue);
  }

  setValue(newValue: T): void {
    this.ctrl.setValue(newValue);
  }

  setValueWithoutTrigger(newValue: T): void {
    this.ctrl.setValue(newValue, {emitEvent: false});
    this.value = newValue;
  }

  destroy(): void {
    this.valueChangedSub.unsubscribe();
  }
}
