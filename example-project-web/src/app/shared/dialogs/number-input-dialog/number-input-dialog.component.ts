import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {UntypedFormBuilder, UntypedFormGroup, Validators} from '@angular/forms';

export interface TextInputDialogData {
  title: string;
  text: string;
  label: string;
  defaultValue?: string;
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
  maxValue: number;
  minValue: number;
  inputForm: UntypedFormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: TextInputDialogData,
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

    this.inputForm = this._fb.group({
      inputValue: [this.data.defaultValue, Validators.required],
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
