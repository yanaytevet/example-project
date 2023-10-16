import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
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
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {MatInputModule} from '@angular/material/input';
import {MatSelectModule} from '@angular/material/select';
import {ClipboardModule} from '@angular/cdk/clipboard';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {PaginationTableComponent} from './components/pagination-tables/pagination-table/pagination-table.component';
import {MatTableModule} from '@angular/material/table';
import {PaginatorComponent} from './components/pagination-tables/paginator/paginator.component';
import {ColumnOptionsFilterComponent} from './components/pagination-tables/column-filter/column-options-filter.component';
import {MatMenuModule} from '@angular/material/menu';
import {MatSortModule} from '@angular/material/sort';
import {KeyValueDialogComponent} from './dialogs/key-value-dialog/key-value-dialog.component';
import {BreadcrumbsComponent} from './components/breadcrumbs/breadcrumbs.component';
import {RouterLink} from '@angular/router';
import {
  ColumnTextFilterComponent
} from './components/pagination-tables/column-text-filter/column-text-filter.component';
import {
  ChipsAutocompleteDragComponent
} from './components/chips/chips-autocomplete-drag/chips-autocomplete-drag.component';
import {ChipsListInputComponent} from './components/chips/chips-list-input/chips-list-input.component';
import {MatChipsModule} from '@angular/material/chips';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {CdkDrag, CdkDropList} from '@angular/cdk/drag-drop';
import {DisplayTextComponent} from './components/texts/display-text/display-text.component';


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
    KeyValueDialogComponent,
    PaginationTableComponent,
    PaginatorComponent,
    ColumnOptionsFilterComponent,
    ColumnTextFilterComponent,
    BreadcrumbsComponent,
    ChipsAutocompleteDragComponent,
    ChipsListInputComponent,
    DisplayTextComponent
  ],
  exports: [
    PaginationTableComponent,
    ColumnOptionsFilterComponent,
    ColumnTextFilterComponent,
    BreadcrumbsComponent,
    ChipsAutocompleteDragComponent,
    ChipsListInputComponent,
    DisplayTextComponent
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
    MatCheckboxModule,
    MatTableModule,
    MatMenuModule,
    FormsModule,
    MatSortModule,
    RouterLink,
    MatChipsModule,
    MatAutocompleteModule,
    CdkDropList,
    CdkDrag
  ]
})
export class SharedModule {
}
