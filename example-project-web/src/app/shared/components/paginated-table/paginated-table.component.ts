import {Component, computed, inject, input, TemplateRef, ViewChild} from '@angular/core';
import {ColumnMode, NgxDatatableModule, PageEvent, SortEvent, SortType, TableColumn} from '@swimlane/ngx-datatable';
import {PaginatedTableHandler} from './paginated-table-handler';
import {PaginationInput} from './pagination-input';
import {PaginatedData} from './paginated-data';
import {MenuButtonComponent} from '../menu-button/menu-button.component';
import {TableAction} from './table-action';
import {Action} from '../../interfaces/util/action';
import {bootstrapThreeDotsVertical} from '@ng-icons/bootstrap-icons';
import {DarkModeService} from '../../services/dark-mode.service';
import {PaginatedTableColumn} from './paginated-table-column';
import {ColumnFilterComponent} from './filters/column-filter/column-filter.component';

@Component({
  selector: 'app-paginated-table',
  imports: [
    NgxDatatableModule,
    MenuButtonComponent,
    ColumnFilterComponent
  ],
  templateUrl: './paginated-table.component.html'
})
export class PaginatedTableComponent<T, S extends PaginationInput> {
  @ViewChild('actionTmpl', { static: true }) actionTmpl: TemplateRef<any>;
  @ViewChild('colHeader', { static: true }) colHeaderTpl!: TemplateRef<any>;
  themeService = inject(DarkModeService);

  paginatedDataHandler = input<PaginatedTableHandler<T, S>>();

  paginationDataSignal = computed<PaginatedData<T>>(() => {
    if (!this.paginatedDataHandler()){
      return null;
    }
    return this.paginatedDataHandler().paginationDataSignal();
  });
  columns = input<PaginatedTableColumn[]>();
  actions = input<TableAction[]>();
  realColumns = computed<TableColumn[]>(() => {
    const columns = this.columns().map((column => {
      if (column.filter) {
        return {
          ...column,
          headerTemplate: this.colHeaderTpl,
        };
      }
      return column;
    }));

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
    const paginatedDataHandler = this.paginatedDataHandler()
    if (paginatedDataHandler && paginatedDataHandler.pageSize === $event.pageSize && paginatedDataHandler.currentPage === $event.offset) {
      return;
    }
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
