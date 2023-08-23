import {Injectable} from '@angular/core';
import {firstValueFrom} from 'rxjs';
import {MatDialog} from '@angular/material/dialog';
import {ConfirmationDialogComponent, ConfirmationDialogData} from './confirmation-dialog/confirmation-dialog.component';
import {TextInputDialogComponent, TextInputDialogData} from './text-input-dialog/text-input-dialog.component';
import {NumberInputDialogComponent, NumberInputDialogData} from './number-input-dialog/number-input-dialog.component';
import {
  NotificationTextDialogComponent,
  NotificationTextDialogData
} from './notification-text-dialog/notification-text-dialog.component';
import {
  ListSingleSelectionDialogComponent, ListSingleSelectionDialogData
} from './list-single-selection-dialog/list-single-selection-dialog.component';
import {
  ListSelectionDialogComponent,
  ListSelectionDialogData
} from './list-selection-dialog/list-selection-dialog.component';
import {KeyValueDialogComponent} from './key-value-dialog/key-value-dialog.component';
@Injectable({
  providedIn: 'root'
})
export class DialogsService {

  constructor(private matDialog: MatDialog) {
  }

  public async showNotificationDialog(data: NotificationTextDialogData): Promise<void> {
    const dialogRef = this.matDialog.open(NotificationTextDialogComponent, {
      width: '400px',
      data
    });
    await firstValueFrom<void>(dialogRef.afterClosed());
  }

  public async getBooleanFromConfirmationDialog(data: ConfirmationDialogData): Promise<boolean> {
    const dialogRef = this.matDialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data
    });
    return await firstValueFrom<boolean>(dialogRef.afterClosed());
  }

  public async getStringFromInputDialog(data: TextInputDialogData): Promise<string> {
    const dialogRef = this.matDialog.open(TextInputDialogComponent, {
      width: '400px',
      data,
    });
    return await firstValueFrom<string>(dialogRef.afterClosed());
  }

  public async getNumberFromInputDialog(data: NumberInputDialogData): Promise<number> {
    const dialogRef = this.matDialog.open(NumberInputDialogComponent, {
      width: '400px',
      data
    });
    return await firstValueFrom<number>(dialogRef.afterClosed());
  }

  public async getSingleOptionFromListDialog<T>(data: ListSingleSelectionDialogData): Promise<T> {
    const dialogRef = this.matDialog.open(ListSingleSelectionDialogComponent, {
      width: '400px',
      data
    });
    return await firstValueFrom<T>(dialogRef.afterClosed());
  }

  public async getMultiOptionsFromListDialog<T>(data: ListSelectionDialogData): Promise<T[]> {
    const dialogRef = this.matDialog.open(ListSelectionDialogComponent, {
      width: '400px',
      data
    });
    return await firstValueFrom<T[]>(dialogRef.afterClosed());
  }

  async getKeyValueFromDialog(data: any, width?: string): Promise<Record<string, string>> {
    const dialogRef = this.matDialog.open(KeyValueDialogComponent, {
      width: width || '400px',
      data
    });
    return await firstValueFrom<Record<string, string>>(dialogRef.afterClosed());
  }
}
