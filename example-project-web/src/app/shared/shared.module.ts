import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {VarDirective} from './directives/ng-var.directive';
import {BaseComponent} from './components/base-component';
import {ConfirmationDialogComponent} from './dialogs/confirmation-dialog/confirmation-dialog.component';
import {ListSelectionDialogComponent} from './dialogs/list-selection-dialog/list-selection-dialog.component';
import {
  ListSingleSelectionDialogComponent
} from './dialogs/list-single-selection-dialog/list-single-selection-dialog.component';
import {NotificationTextDialogComponent} from './dialogs/notification-text-dialog/notification-text-dialog.component';
import {NumberInputDialogComponent} from './dialogs/number-input-dialog/number-input-dialog.component';
import {TextInputDialogComponent} from './dialogs/text-input-dialog/text-input-dialog.component';
import {MatIconModule} from '@angular/material/icon';
import {MatDialogModule} from '@angular/material/dialog';
import {MatButtonModule} from '@angular/material/button';
import {ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {ClipboardModule} from '@angular/cdk/clipboard';
import {MatCheckboxModule} from '@angular/material/checkbox';



@NgModule({
  declarations: [
    VarDirective,
    BaseComponent,
    ConfirmationDialogComponent,
    ListSelectionDialogComponent,
    ListSingleSelectionDialogComponent,
    NotificationTextDialogComponent,
    NumberInputDialogComponent,
    TextInputDialogComponent,
  ],
  imports: [
    CommonModule,
    MatDialogModule,
    MatIconModule,
    MatButtonModule,
    ReactiveFormsModule,
    MatInputModule,
    MatSelectModule,
    ClipboardModule,
    MatCheckboxModule
  ]
})
export class SharedModule { }
