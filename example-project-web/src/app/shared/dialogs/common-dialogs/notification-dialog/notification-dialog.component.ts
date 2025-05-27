import {Component} from '@angular/core';
import {BaseDialogComponent} from '../../base-dialog.component';
import {CommonModule} from '@angular/common';

export interface NotificationDialogInput {
  title: string;
  text: string;
  confirmActionName?: string;
  showCopyButton?: boolean;
}

@Component({
  selector: 'app-notification-dialog',
  imports: [CommonModule],
  templateUrl: './notification-dialog.component.html',
  standalone: true
})
export class NotificationDialogComponent extends BaseDialogComponent<
    NotificationDialogInput,
    void
> {
  copyToClipboard(): void {
    if (this.data.text) {
      navigator.clipboard.writeText(this.data.text)
        .catch(err => console.error('Could not copy text: ', err));
    }
  }
}
