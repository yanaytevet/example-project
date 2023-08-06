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
  inputType?: string;
  isTextArea?: boolean;
  textAreaRows?: number;
  maxLength?: number;
  allowEmpty?: boolean;
}

@Component({
  selector: 'app-text-input-dialog',
  templateUrl: './text-input-dialog.component.html',
  styleUrls: ['./text-input-dialog.component.scss']
})
export class TextInputDialogComponent implements OnInit {
  title = '';
  text = '';
  label = '';
  cancelActionName = 'Cancel';
  confirmActionName = 'Confirm';
  inputType = 'text';
  isTextArea = false;
  allowEmpty = false;
  textAreaRows = 3;
  maxLength: number = null;
  inputForm: UntypedFormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: TextInputDialogData,
    public dialogRef: MatDialogRef<TextInputDialogComponent>,
    private _fb: UntypedFormBuilder,
  ) {
    this.title = data.title;
    this.text = data.text;
    this.label = data.label;
    if (this.data.cancelActionName) {
      this.cancelActionName = this.data.cancelActionName;
    }
    if (this.data.isTextArea !== undefined) {
      this.isTextArea = this.data.isTextArea;
    }
    if (this.data.textAreaRows) {
      this.textAreaRows = this.data.textAreaRows;
    }
    if (this.data.confirmActionName) {
      this.confirmActionName = this.data.confirmActionName;
    }
    if (this.data.inputType) {
      this.inputType = this.data.inputType;
    }
    if (this.data.allowEmpty !== undefined) {
      this.allowEmpty = this.data.allowEmpty;
    }
    if (this.data.maxLength) {
      this.maxLength = this.data.maxLength;
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
    if (this.isTextArea) {
      return;
    }
    if (!this.allowEmpty && !this.inputForm.valid) {
      return;
    }
    this.dialogRef.close(this.getValue());
  }
}
