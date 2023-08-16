import {Component} from '@angular/core';
import {BaseComponent} from '../../shared/components/base-component';
import {DialogsService} from '../../shared/dialogs/dialogs.service';

@Component({
  selector: 'app-dialogs-example-page',
  templateUrl: './dialogs-example-page.component.html',
  styleUrls: ['./dialogs-example-page.component.scss']
})
export class DialogsExamplePageComponent extends BaseComponent{
  results: any;

  constructor(private dialogsService: DialogsService) {
    super();
  }

  async showNotificationDialog(): Promise<void> {
   this.results = await this.dialogsService.showNotificationDialog({
      title: 'Notification Dialog',
      text: 'This is a notification dialog.',
      confirmActionName: 'Close',
     showCopyButton: true,
    });
  }

  async getBooleanFromConfirmationDialog(): Promise<void> {
    this.results = await this.dialogsService.getBooleanFromConfirmationDialog({
      title: 'Confirmation Dialog',
      text: 'This is a confirmation dialog. Do you want to continue?',
      cancelActionName: 'No',
      confirmActionName: 'Yes',
    });
  }

  async getStringFromInputDialog(): Promise<void> {
    this.results = await this.dialogsService.getStringFromInputDialog({
      title: 'Input Dialog',
      text: 'This is an input dialog. Please enter some text.',
      label: 'Text',
      defaultValue: 'Hello World',
      cancelActionName: 'Cancel',
      confirmActionName: 'Confirm',
      inputType: 'text',
      isTextArea: false,
      maxLength: 100,
      allowEmpty: false,
    });
  }

  async getNumberFromInputDialog(): Promise<void> {
    this.results = await this.dialogsService.getNumberFromInputDialog({
      title: 'Input Dialog',
      text: 'This is an input dialog. Please enter a number.',
      label: 'Number',
      defaultValue: 42,
      cancelActionName: 'Cancel',
      confirmActionName: 'Confirm',
      allowEmpty: false,
      maxValue: 100,
      minValue: -5,
    });
  }

  async getSingleOptionFromListDialog(): Promise<void> {
    this.results = await this.dialogsService.getSingleOptionFromListDialog<number>({
      title: 'List Dialog',
      text: 'This is a list dialog. Please select an option.',
      label: 'Option',
      options: [
        {display: 'Option 1', value: 1},
        {display: 'Option 2', value: 2},
        {display: 'Option 3', value: 3},
      ],
      defaultValue: 2,
      cancelActionName: 'Cancel',
      confirmActionName: 'Confirm',
      allowEmpty: false,
    });
  }

  async getMultiOptionsFromListDialog(): Promise<void> {
    this.results = await this.dialogsService.getMultiOptionsFromListDialog<number>({
      title: 'List Dialog',
      text: 'This is a list dialog. Please select an option.',
      options: [
        {display: 'Option 1', value: 1, isChecked: true},
        {display: 'Option 2', value: 2},
        {display: 'Option 3', value: 3, isChecked: true},
      ],
      cancelActionName: 'Cancel',
      confirmActionName: 'Confirm',
    });
  }
}
