import {Component, input, signal} from '@angular/core';
import {ControlValueAccessor, FormsModule, NG_VALUE_ACCESSOR, ReactiveFormsModule} from '@angular/forms';

@Component({
    selector: 'app-checkbox-input',
    templateUrl: './checkbox-input.component.html',
    imports: [
        ReactiveFormsModule,
        FormsModule
    ],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            useExisting: CheckboxInputComponent,
            multi: true,
        }
    ]
})
export class CheckboxInputComponent implements ControlValueAccessor {
    label = input<string>();
    value = signal(false);
    disabled = signal(false);

    // Called by Angular to write a value from the form model into the view
    writeValue(val: boolean): void {
        this.value.set(val ?? false);
    }

    // Register a function to propagate changes
    onChange: (value: boolean) => void = () => {
    };

    registerOnChange(fn: (value: boolean) => void): void {
        this.onChange = fn;
    }

    // Register a function to mark control as touched
    onTouched: () => void = () => {
    };

    registerOnTouched(fn: () => void): void {
        this.onTouched = fn;
    }

    // Support disabled state
    setDisabledState(isDisabled: boolean): void {
        this.disabled.set(isDisabled);
    }

    // Handle input event from native input
    onInput(event: Event) {
        const newValue = (event.target as HTMLInputElement).checked;
        this.value.set(newValue);
        this.onChange(newValue);
    }
}
