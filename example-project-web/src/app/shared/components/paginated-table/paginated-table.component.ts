import {Component, computed, input, TemplateRef, ViewChild} from '@angular/core';
import {ColumnMode, NgxDatatableModule, PageEvent, SortEvent, SortType, TableColumn} from '@swimlane/ngx-datatable';
import {PaginatedTableHandler} from './paginated-table-handler';
import {PaginationInput} from './pagination-input';
import {PaginatedData} from './paginated-data';
import {MenuButtonComponent} from '../menu-button/menu-button.component';
import {TableAction} from './table-action';
import {Action} from '../../interfaces/util/action';
import {bootstrapThreeDotsVertical} from '@ng-icons/bootstrap-icons';

@Component({
  selector: 'app-paginated-table',
  imports: [
    NgxDatatableModule,
    MenuButtonComponent
  ],
  templateUrl: './paginated-table.component.html',
  styleUrl: './paginated-table.component.css'
})
export class PaginatedTableComponent<T, S extends PaginationInput> {
  @ViewChild('actionTmpl', { static: true }) actionTmpl: TemplateRef<any>;

  paginatedDataHandler = input<PaginatedTableHandler<T, S>>();

  paginationDataSignal = computed<PaginatedData<T>>(() => {
    if (!this.paginatedDataHandler()){
      return null;
    }
    return this.paginatedDataHandler().paginationDataSignal();
  });
  columns = input<TableColumn[]>();
  actions = input<TableAction[]>();
  realColumns = computed<TableColumn[]>(() => {
    const columns = this.columns();
    const actions = this.actions();
    if (actions) {
      columns.push(
          {prop: 'action', name: ' ', sortable: false, width: 10,
          cellTemplate: this.actionTmpl},
      )
    }
    return columns;
  });

  setPage($event: PageEvent) {
    this.paginatedDataHandler()?.fetchPage($event.offset, $event.pageSize);
  }

  setSort($event: SortEvent) {
    const paginatedDataHandler = this.paginatedDataHandler()
    paginatedDataHandler.clearAllSort(false)
    $event.sorts.forEach(sortProp => {
      paginatedDataHandler.addSort(sortProp.prop as string, sortProp.dir, false)
    });
    paginatedDataHandler.fetch();
  }

  getActions(row: any): Action[] {
    return this.actions().map((tableAction) => {
      return {
        display: tableAction.display,
        icon: tableAction.icon,
        callback: () => {
          tableAction.callback(row);
        },
      }
    });
  }

  protected readonly ColumnMode = ColumnMode;
  protected readonly SortType = SortType;
  protected readonly bootstrapThreeDotsVertical = bootstrapThreeDotsVertical;
}
