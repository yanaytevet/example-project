import {Component, inject} from '@angular/core';
import {PaginatedTableComponent} from '../shared/components/paginated-table/paginated-table.component';
import {PaginatedTableHandler} from '../shared/components/paginated-table/paginated-table-handler';
import {
    BlockSchema, deleteBlockItemView,
    paginationBlockView,
    PaginationBlockViewData, readBlockItemView,
    runActionBuildBlockItemView, updateBlockItemView
} from '../../generated-files/api/blocks';
import {BasePageComponent} from '../shared/components/base-page-component';
import {TableAction} from '../shared/components/paginated-table/table-action';
import {featherActivity, featherBookOpen, featherDelete, featherEdit} from '@ng-icons/feather-icons';
import {BreadcrumbsComponent} from '../shared/components/breadcrumbs/breadcrumbs.component';
import {BreadcrumbsService} from '../shared/components/breadcrumbs/breadcrumbs.service';
import {StringUtilsService} from '../shared/services/string-utils.service';
import {DialogService} from '../shared/dialogs/dialogs.service';
import {InputDebounce} from '../shared/data/input-debouncer';
import {ReactiveFormsModule} from '@angular/forms';
import {PaginatedTableColumn} from '../shared/components/paginated-table/paginated-table-column';

@Component({
    selector: 'app-example-table',
    imports: [PaginatedTableComponent, BreadcrumbsComponent, ReactiveFormsModule],
    templateUrl: './example-table.component.html',
    styleUrl: './example-table.component.css'
})
export class ExampleTableComponent extends BasePageComponent {
    breadcrumbsService = inject(BreadcrumbsService);
    stringUtilsService = inject(StringUtilsService);
    dialogsService = inject(DialogService);

    columns: PaginatedTableColumn[] = [
        {prop: 'id'},
        {prop: 'a'},
        {prop: 'b'},
        {prop: 'c'},
        {prop: 'block_type', name: 'Block Type', sortable: false},
    ]

    actions: TableAction[] = [
        {
            display: 'Show Details', icon: featherBookOpen, callback: async (block: BlockSchema) => {
                const fullBlock = await readBlockItemView({
                    path: {object_id: block.id}
                });
                await this.dialogsService.showNotificationDialog({
                    title: `Block ${block.id}`,
                    text: JSON.stringify(fullBlock, null, 2),
                });
            }
        },
        {
            display: 'Delete', icon: featherDelete, callback: async (block: BlockSchema) => {
                await deleteBlockItemView({
                    path: {object_id: block.id}
                });
                await this.paginatedDataHandler.fetch();
            }
        },
        {
            display: 'Update', icon: featherEdit, callback: async (block: BlockSchema) => {
                await updateBlockItemView({
                    body: {
                        a: this.stringUtilsService.generateRandomString(10),
                        b: Math.floor(Math.random() * 11),
                        c: Math.random() < 0.5,
                    },
                    path: {
                        object_id: block.id,
                    }
                });
                await this.paginatedDataHandler.fetch();
            }
        },
        {
            display: 'Build', icon: featherActivity, callback: async (block: BlockSchema) => {
                await runActionBuildBlockItemView({
                    body: {
                        should_build: true,
                    },
                    path: {
                        object_id: block.id,
                    }
                });
                await this.paginatedDataHandler.fetch();
            }
        },
    ];

    paginatedDataHandler: PaginatedTableHandler<BlockSchema, PaginationBlockViewData> = null;
    searchDebouncer = new InputDebounce('');

    constructor() {
        super();
        this.paginatedDataHandler = new PaginatedTableHandler<BlockSchema, PaginationBlockViewData>(async (options) => {
            return (await paginationBlockView(options)).data;
        });
        this.paginatedDataHandler.fetch();
        this.breadcrumbs = this.breadcrumbsService.getExampleTableBreadcrumbs();
        this.subscriptions.push(this.searchDebouncer.valueChangedFinished$.subscribe(
            value => {
                this.paginatedDataHandler.setFilter('search', value)
            }
        ))
    }

    override ngOnDestroy() {
        super.ngOnDestroy();
        this.paginatedDataHandler.destroy();
    }
}
