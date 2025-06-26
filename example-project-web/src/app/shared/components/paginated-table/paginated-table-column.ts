import {TableColumn} from '@swimlane/ngx-datatable';
import {PaginatedTableFilter} from './filters/paginated-table-filter';

export interface PaginatedTableColumn extends TableColumn {
    filter?: PaginatedTableFilter;
}
