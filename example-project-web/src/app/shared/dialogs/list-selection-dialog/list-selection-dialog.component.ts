import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {UntypedFormControl, UntypedFormGroup} from '@angular/forms';

export interface ListSelectionOption {
  display: string;
  value: string;
  isChecked?: boolean;
}
export interface ListSelectionDialogData {
  title: string;
  text: string;
  options: ListSelectionOption[];
  cancelActionName?: string;
  confirmActionName?: string;
}

@Component({
  selector: 'app-list-selection-dialog',
  templateUrl: './list-selection-dialog.component.html',
  styleUrls: ['./list-selection-dialog.component.scss']
})
export class ListSelectionDialogComponent implements OnInit {
  title = '';
  text = '';
  cancelActionName = 'Cancel';
  confirmActionName = 'Confirm';
  valuesList: string[];
  valueToDisplay: Record<string, string>;
  form: UntypedFormGroup;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: ListSelectionDialogData,
    public dialogRef: MatDialogRef<ListSelectionDialogComponent>,
  ) {
    this.title = data.title;
    this.text = data.text;
    if (this.data.cancelActionName) {
      this.cancelActionName = this.data.cancelActionName;
    }
    if (this.data.confirmActionName) {
      this.confirmActionName = this.data.confirmActionName;
    }

    this.valuesList = data.options.map(option => option.value);
    const valueToDisplay: Record<string, string> = {};
    this.form = new UntypedFormGroup({});

    data.options.forEach(option => {
      valueToDisplay[option.value] = option.display;
      this.form.addControl(option.value, new UntypedFormControl(!!option.isChecked));
    })
    this.valueToDisplay = valueToDisplay;
  }

  ngOnInit(): void {
  }

  submitList() {
    const valueToChecked = this.form.value;
    const res: string[] = [];
    Object.keys(valueToChecked).forEach(value => {
      if (valueToChecked[value]) {
        res.push(value);
      }
    })
    this.dialogRef.close(res);
  }
}
