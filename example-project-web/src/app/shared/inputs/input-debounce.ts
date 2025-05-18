import {debounceTime, distinctUntilChanged} from 'rxjs/operators';
import {BehaviorSubject, Observable, Subject} from 'rxjs';
import {FormControl} from '@angular/forms';
import {InputDebouceStatus} from '../interfaces/util/input-debouce-status';

export class InputDebounce<T> {
  valueChangedSub: Subject<T> = new Subject<T>();
  valueChangedFinishedSub: Subject<T> = new Subject<T>();
  valueChangedFinished$: Observable<T> = this.valueChangedFinishedSub.asObservable();
  debounceStatus: BehaviorSubject<InputDebouceStatus> = new BehaviorSubject<InputDebouceStatus>('idle');
  value: T = null;
  ctrl = new FormControl<T>(null);

  constructor(initValue?: T) {
    this.valueChangedSub.pipe(
      debounceTime(1000),
      distinctUntilChanged())
      .subscribe( newValue => {
        this.value = newValue;
        this.valueChangedFinishedSub.next(newValue);
        this.debounceStatus.next('idle');
      });

    this.ctrl.valueChanges.subscribe(event => {
      this.onValueChangedInCtrl(event);
    });

    if (initValue !== undefined) {
      this.setValueWithoutTrigger(initValue);
    }
  }

  onValueChangedInCtrl(newValue: T): void {
    this.debounceStatus.next('working');
    this.valueChangedSub.next(newValue);
  }

  setValue(newValue: T): void {
    this.ctrl.setValue(newValue);
  }

  setValueWithoutTrigger(newValue: T): void {
    this.ctrl.setValue(newValue, {emitEvent: false,onlySelf: true});
    this.value = newValue;
  }

  destroy(): void {
    this.valueChangedSub.unsubscribe();
  }
}
