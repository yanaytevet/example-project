import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {UntypedFormBuilder, UntypedFormGroup, ValidatorFn, Validators} from '@angular/forms';

export interface NumberInputDialogData {
  title: string;
  text: string;
  label: string;
  defaultValue?: number;
  cancelActionName?: string;
  confirmActionName?: string;
  allowEmpty?: boolean;
  maxValue?: number;
  minValue?: number;
}

@Component({
  selector: 'app-number-input-dialog',
  templateUrl: './number-input-dialog.component.html',
  styleUrls: ['./number-input-dialog.component.scss']
})
export class NumberInputDialogComponent implements OnInit {
  title = '';
  text = '';
  label = '';
  cancelActionName = 'Cancel';
  confirmActionName = 'Confirm';
  allowEmpty = false;
  maxValue: number = null;
  minValue: number = null;
  inputForm: UntypedFormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: NumberInputDialogData,
    public dialogRef: MatDialogRef<NumberInputDialogComponent>,
    private _fb: UntypedFormBuilder,
  ) {
    this.title = data.title;
    this.text = data.text;
    this.label = data.label;
    if (this.data.cancelActionName) {
      this.cancelActionName = this.data.cancelActionName;
    }
    if (this.data.confirmActionName) {
      this.confirmActionName = this.data.confirmActionName;
    }
    if (this.data.allowEmpty) {
      this.allowEmpty = this.data.allowEmpty;
    }
    if (this.data.maxValue) {
      this.maxValue = this.data.maxValue;
    }
    if (this.data.minValue) {
      this.minValue = this.data.minValue;
    }

    const validators: ValidatorFn[] = [];
    if (this.maxValue !== null) {
      validators.push(Validators.max(this.maxValue));
    }
    if (this.minValue !== null) {
      validators.push(Validators.min(this.minValue));
    }
    if (!this.allowEmpty) {
      validators.push(Validators.required);
    }

    this.inputForm = this._fb.group({
      inputValue: [this.data.defaultValue, validators],
    });
  }

  ngOnInit(): void {
  }

  getValue(): string {
    return this.inputForm.controls['inputValue'].value;
  }

  clickedEnter() {
    if (!this.allowEmpty && !this.inputForm.valid) {
      return;
    }
    this.dialogRef.close(this.getValue());
  }
}
