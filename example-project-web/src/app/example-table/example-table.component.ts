import {Component, inject} from '@angular/core';
import {PaginatedTableComponent} from '../shared/components/paginated-table/paginated-table.component';
import {PaginatedTableHandler} from '../shared/components/paginated-table/paginated-table-handler';
import {BlockSchema, paginationBlockView, PaginationBlockViewData} from '../../generated-files/api/blocks';
import {BasePageComponent} from '../shared/components/base-page-component';
import {TableAction} from '../shared/components/paginated-table/table-action';
import {featherActivity, featherBookOpen, featherDelete, featherEdit} from '@ng-icons/feather-icons';
import {BreadcrumbsComponent} from '../shared/components/breadcrumbs/breadcrumbs.component';
import {BreadcrumbsService} from '../shared/components/breadcrumbs/breadcrumbs.service';
import {LinkItem} from '../shared/components/breadcrumbs/link-item';

@Component({
    selector: 'app-example-table',
    imports: [PaginatedTableComponent, BreadcrumbsComponent],
    templateUrl: './example-table.component.html',
    styleUrl: './example-table.component.css'
})
export class ExampleTableComponent extends BasePageComponent {
    breadcrumbsService = inject(BreadcrumbsService);

    columns = [
        {prop: 'id'},
        {prop: 'a'},
        {prop: 'b'},
        {prop: 'c'},
        {prop: 'block_type', name: 'Block Type', sortable: false},
    ]

    actions: TableAction[] = [
        {
            display: 'Show Details', icon: featherBookOpen, callback: (block: BlockSchema) => {

            }
        },
        {
            display: 'Delete', icon: featherDelete, callback: (block: BlockSchema) => {

            }
        },
        {
            display: 'Update', icon: featherEdit, callback: (block: BlockSchema) => {

            }
        },
        {
            display: 'Build', icon: featherActivity, callback: (block: BlockSchema) => {

            }
        },
    ];

    paginatedDataHandler: PaginatedTableHandler<BlockSchema, PaginationBlockViewData> = null;

    constructor() {
        super();
        this.paginatedDataHandler = new PaginatedTableHandler<BlockSchema, PaginationBlockViewData>(async (options) => {
            return (await paginationBlockView(options)).data;
        });
        this.paginatedDataHandler.fetch();
        this.breadcrumbs = this.breadcrumbsService.getExampleTableBreadcrumbs();
    }

    override ngOnDestroy() {
        super.ngOnDestroy();
        this.paginatedDataHandler.destroy();
    }
}
