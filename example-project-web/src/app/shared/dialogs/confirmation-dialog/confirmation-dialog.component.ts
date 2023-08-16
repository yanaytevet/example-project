import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

export interface ConfirmationDialogData {
  title: string;
  text: string;
  cancelActionName?: string;
  confirmActionName?: string;
}

@Component({
  selector: 'app-confirmation-dialog',
  templateUrl: './confirmation-dialog.component.html',
  styleUrls: ['./confirmation-dialog.component.scss'],
})
export class ConfirmationDialogComponent implements OnInit {
  title = '';
  text = '';
  cancelActionName = 'Cancel';
  confirmActionName = 'Confirm';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: ConfirmationDialogData,
    public dialogRef: MatDialogRef<ConfirmationDialogComponent>,
  ) {
    this.title = data.title;
    this.text = data.text;
    if (this.data.cancelActionName) {
      this.cancelActionName = this.data.cancelActionName;
    }
    if (this.data.confirmActionName) {
      this.confirmActionName = this.data.confirmActionName;
    }
  }

  ngOnInit(): void {
  }

}
