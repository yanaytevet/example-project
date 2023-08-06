import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

export interface NotificationTextDialogData {
  title: string;
  text: string;
  confirmActionName?: string;
}

@Component({
  selector: 'app-notification-text-dialog',
  templateUrl: './notification-text-dialog.component.html',
  styleUrls: ['./notification-text-dialog.component.scss']
})
export class NotificationTextDialogComponent implements OnInit {
  title = '';
  text = '';
  label = '';
  confirmActionName = 'Close';

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: NotificationTextDialogData,
    public dialogRef: MatDialogRef<NotificationTextDialogComponent>,
  ) {
    this.title = data.title;
    this.text = data.text;
    if (this.data.confirmActionName) {
      this.confirmActionName = this.data.confirmActionName;
    }
  }

  ngOnInit(): void {
  }
}
