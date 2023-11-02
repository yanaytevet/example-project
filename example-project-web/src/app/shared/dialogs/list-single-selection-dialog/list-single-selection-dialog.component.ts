import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

export interface ListSingleSelectionOption {
  display: string;
  value: any;
}
export interface ListSingleSelectionDialogData {
  title: string;
  text: string;
  options: ListSingleSelectionOption[];
  defaultValue?: any;
  cancelActionName?: string;
  confirmActionName?: string;
  allowEmpty?: boolean;
  label?: string;
  multiButtons?: boolean;
}

@Component({
  selector: 'app-list-single-selection-dialog',
  templateUrl: './list-single-selection-dialog.component.html',
  styleUrls: ['./list-single-selection-dialog.component.scss']
})
export class ListSingleSelectionDialogComponent implements OnInit {
  title = '';
  text = '';
  cancelActionName = 'Cancel';
  confirmActionName = 'Confirm';
  label = 'Select an option';
  selectedValue: any = null;
  allowEmpty = false
  multiButtons = false

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: ListSingleSelectionDialogData,
    public dialogRef: MatDialogRef<ListSingleSelectionDialogComponent>,
  ) {
    this.title = data.title;
    this.text = data.text;
    if (this.data.cancelActionName) {
      this.cancelActionName = this.data.cancelActionName;
    }
    if (this.data.confirmActionName) {
      this.confirmActionName = this.data.confirmActionName;
    }
    if (this.data.label) {
      this.label = this.data.label;
    }
    if (this.data.multiButtons) {
      this.multiButtons = this.data.multiButtons;
    }
    this.selectedValue = this.data.defaultValue ? this.data.defaultValue : null;
    this.allowEmpty = !!this.data.allowEmpty;
  }

  ngOnInit(): void {
  }

  submit() {
    this.dialogRef.close(this.selectedValue);
  }

  get isValid(): boolean {
    if (this.allowEmpty) {
      return true;
    }
    return !!this.selectedValue;
  }

  submitValue(value: string) {
    this.selectedValue = value;
    this.submit();
  }
}
