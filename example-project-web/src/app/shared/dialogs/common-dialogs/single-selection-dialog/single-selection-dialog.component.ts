import { Component, OnInit } from '@angular/core';
import { BaseDialogComponent } from '../../base-dialog.component';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { NgIcon } from '@ng-icons/core';
import { bootstrapChevronDown } from '@ng-icons/bootstrap-icons';
import { ConfirmationButtonComponent } from '../../confirmation-button/confirmation-button.component';

export interface SingleSelectionOption {
  display: string;
  value: any;
}

export interface SingleSelectionDialogInput {
  title: string;
  text: string;
  options: SingleSelectionOption[];
  defaultValue?: any;
  cancelActionName?: string;
  confirmActionName?: string;
  allowEmpty?: boolean;
  label?: string;
  method?: 'buttons' | 'dropdown'; // the default is dropdown
}

@Component({
  selector: 'app-single-selection-dialog',
  imports: [ReactiveFormsModule, CommonModule, NgIcon, ConfirmationButtonComponent],
  templateUrl: './single-selection-dialog.component.html',
  standalone: true
})
export class SingleSelectionDialogComponent extends BaseDialogComponent<
  SingleSelectionDialogInput,
  any
> implements OnInit {
  form: FormGroup;
  selectedOption: any = null;
  protected readonly chevronDownIcon = bootstrapChevronDown;

  constructor(private fb: FormBuilder) {
    super();
  }

  ngOnInit(): void {
    this.form = this.fb.group({
      selectedValue: [
        this.data.defaultValue ?? '',
        this.buildValidators()
      ]
    });

    // Set default value if provided
    if (this.data.defaultValue !== undefined) {
      this.selectedOption = this.data.defaultValue;
      this.form.get('selectedValue')?.setValue(this.data.defaultValue);
    }
  }

  private buildValidators() {
    const validators = [];

    if (this.data.allowEmpty !== true) {
      validators.push(Validators.required);
    }

    return validators;
  }

  get selectionControl() {
    return this.form.get('selectedValue');
  }

  hasError(errorName: string): boolean {
    return this.selectionControl?.errors?.[errorName] &&
           (this.selectionControl.touched || this.selectionControl.dirty);
  }

  getErrorMessage(): string | null {
    if (this.hasError('required')) {
      return 'Please select an option';
    }

    return null;
  }

  onConfirm(): void {
    // Mark form as touched to trigger validation messages
    this.form.markAllAsTouched();

    if (this.form.valid) {
      this.emitClose(this.selectionControl?.value);
    }
  }

  toggleValue(value: any): void {
    // Toggle selection if the same option is clicked again
    if (this.selectedOption === value) {
      this.selectedOption = null;
      this.selectionControl?.setValue('');
    } else {
      this.selectedOption = value;
      this.selectionControl?.setValue(value);
    }
  }

  isSelected(value: any): boolean {
    return this.selectedOption === value;
  }
}
