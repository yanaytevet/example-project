import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {FormGroup, UntypedFormControl, UntypedFormGroup} from '@angular/forms';

export interface ListSelectionOption {
  display: string;
  value: any;
  isChecked?: boolean;
}
export interface ListSelectionDialogData {
  title: string;
  text: string;
  options: ListSelectionOption[];
  cancelActionName?: string;
  confirmActionName?: string;
  allowEmpty?: boolean;
}

@Component({
  selector: 'app-list-selection-dialog',
  templateUrl: './list-selection-dialog.component.html',
  styleUrls: ['./list-selection-dialog.component.scss']
})
export class ListSelectionDialogComponent implements OnInit {
  title = '';
  text = '';
  allowEmpty: boolean = false;
  cancelActionName = 'Cancel';
  confirmActionName = 'Confirm';
  valuesList: any[];
  valueToDisplay: Record<any, string>;
  isValid = false;
  form: FormGroup;

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
    if (this.data.allowEmpty) {
      this.allowEmpty = this.data.allowEmpty;
    }

    this.valuesList = data.options.map(option => option.value);
    const valueToDisplay: Record<string, string> = {};
    this.form = new FormGroup({});

    data.options.forEach(option => {
      valueToDisplay[option.value] = option.display;
      this.form.addControl(option.value, new UntypedFormControl(!!option.isChecked));
    })
    this.valueToDisplay = valueToDisplay;

    this.form.valueChanges.subscribe(() => {
      this.calcIsValid();
    });

    this.calcIsValid();
  }

  calcIsValid(): void {
    if (this.allowEmpty) {
      this.isValid = true;
      return;
    }
    const valueToChecked = this.form.value;
    let isValid = false;
    Object.keys(valueToChecked).forEach(value => {
      if (valueToChecked[value]) {
        isValid = true;
      }
    })
    this.isValid = isValid;
  }

  ngOnInit(): void {
  }

  submitList() {
    const valueToChecked = this.form.value;
    const res: any[] = [];
    this.valuesList.forEach(value => {
      if (valueToChecked[value]) {
        res.push(value);
      }
    });
    this.dialogRef.close(res);
  }
}
