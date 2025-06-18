import {debounceTime, distinctUntilChanged} from 'rxjs/operators';
import {Observable, Subject} from 'rxjs';
import {FormControl} from '@angular/forms';

export class InputDebounce<T> {
    valueChangedSub: Subject<T> = new Subject<T>();
    valueChangedFinishedSub: Subject<T> = new Subject<T>();
    valueChangedFinished$: Observable<T> = this.valueChangedFinishedSub.asObservable();
    value: T = null;
    ctrl = new FormControl<T>(null);

    constructor(initValue?: T, debounceTimeMs = 500) {
        this.valueChangedSub.pipe(
            debounceTime(debounceTimeMs),
            distinctUntilChanged())
            .subscribe( newValue => {
                this.value = newValue;
                this.valueChangedFinishedSub.next(newValue);
            });

        this.ctrl.valueChanges.subscribe(event => {
            this.onValueChangedInCtrl(event);
        });

        if (initValue !== undefined) {
            this.setValueWithoutTrigger(initValue);
        }
    }

    onValueChangedInCtrl(newValue: T): void {
        this.valueChangedSub.next(newValue);
    }

    setValue(newValue: T): void {
        this.ctrl.setValue(newValue);
    }

    setValueImmediately(newValue: T): void {
        this.ctrl.setValue(newValue, {emitEvent: false});
        this.value = newValue;
        this.valueChangedFinishedSub.next(newValue);
    }

    setValueWithoutTrigger(newValue: T): void {
        this.ctrl.setValue(newValue, {emitEvent: false});
        this.value = newValue;
    }

    destroy(): void {
        this.valueChangedSub.unsubscribe();
    }
}
