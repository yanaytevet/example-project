import {Component, inject, signal} from '@angular/core';
import { Action } from '../shared/interfaces/util/action';
import {
  bootstrapQuestion,
  bootstrapBell
} from '@ng-icons/bootstrap-icons';
import {DialogService} from '../shared/dialogs/dialogs.service';
import {CommonModule} from '@angular/common';
import {NgClass} from '@angular/common';
import {NgIconComponent} from '@ng-icons/core';

@Component({
  selector: 'app-example-dialogs',
  imports: [
    CommonModule,
    NgClass,
    NgIconComponent
  ],
  templateUrl: './example-dialogs.component.html',
  styleUrl: './example-dialogs.component.css',
  standalone: true
})
export class ExampleDialogsComponent {
  dialogService  = inject(DialogService);
  data = signal<string>('');

  actions: Action[] = [
    {
      display: 'Confirmation',
      icon: bootstrapQuestion,
      callback: async () => {
        this.setData(await this.dialogService.getBooleanFromConfirmationDialog({
          title: 'Confirmation Dialog',
          text: 'This is a confirmation dialog. Do you want to continue?',
          cancelActionName: 'No',
          confirmActionName: 'Yes',
        }));
      }
    },
    {
      display: 'Notification',
      icon: bootstrapBell,
      callback: async () => {
        await this.dialogService.showNotificationDialog({
          title: 'Notification Dialog',
          text: 'This is a notification dialog with important information.',
          confirmActionName: 'Got it',
          showCopyButton: true,
        });
        this.setData('Notification dialog closed');
      }
    },
  ]

  private setData(val: any) {
    this.data.set(val.toString());
  }
}
