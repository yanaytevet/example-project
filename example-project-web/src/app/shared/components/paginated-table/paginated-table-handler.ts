import {PaginatedData} from './paginated-data';
import {BehaviorSubject, Subscription} from 'rxjs';
import {PaginationInput} from './pagination-input';
import {signal} from '@angular/core';
import {CallbacksDebouncer} from '../../data/callbacks-debouncer';

type SortDirection = 'asc' | 'desc';

interface SortObject {
    direction: SortDirection;
    key: string;
}

export class PaginatedTableHandler<T, S extends PaginationInput> {
    currentPage = 0;
    pageSize = 25;
    isEmpty = true;
    filterObject: Record<string, any> = {};
    sortObjectsArray: SortObject[] = [];
    fetchesDebouncer = new CallbacksDebouncer();

    private readonly _isLoadingSub = new BehaviorSubject<boolean>(true);
    readonly isLoading$ = this._isLoadingSub.asObservable();

    private readonly _paginationDataSub = new BehaviorSubject<PaginatedData<T>>(null);
    readonly paginationData$ = this._paginationDataSub.asObservable();
    readonly paginationDataSignal = signal<PaginatedData<T>>(null);

    sub: Subscription;

    public get isLoading(): boolean {
        return this._isLoadingSub.getValue();
    }

    public set isLoading(val: boolean) {
        this._isLoadingSub.next(val);
    }

    public get paginationData(): PaginatedData<T> {
        return this._paginationDataSub.getValue();
    }

    public set paginationData(val: PaginatedData<T>) {
        this._paginationDataSub.next(val);
        this.isEmpty = val.page_size === 0 && val.pages_amount === 0;
    }

    constructor(private fetchPaginatedData: (val: S) => Promise<PaginatedData<T>>) {
        this.sub = this.paginationData$.subscribe((val: PaginatedData<T>) => {
            this.paginationDataSignal.set(val);
        });
    }

    public async fetch(): Promise<void> {
        this.fetchesDebouncer.run(async () => {
            this.isLoading = true;
            this.currentPage = Math.min(this.currentPage, this.paginationData?.pages_amount - 1 || 0);
            this.currentPage = Math.max(this.currentPage, 0);
            // @ts-ignore
            const data: S = {
                query: {
                    page: this.currentPage,
                    page_size: this.pageSize,
                    order_by: this.getSortArray(),
                    ...this.filterObject
                }
            }
            this.paginationData = await this.fetchPaginatedData(data);
            this.isLoading = false;
        });
    }

    public fetchPage(page: number, pageSize: number, fetch = true): void {
        this.currentPage = page;
        this.pageSize = pageSize;
        if (fetch) {
            this.fetch();
        }
    }

    clearAllFilter(fetch = true): void {
        this.filterObject = {};
        if (fetch) {
            this.fetch();
        }
    }

    setFilter(key: string, value: any, fetch = true): void {
        this.filterObject[key] = value;
        if (fetch) {
            this.fetch();
        }
    }

    clearFilter(key: string, fetch = true): void {
        delete this.filterObject[key];
        if (fetch) {
            this.fetch();
        }
    }

    getFilterValue(key: string): any {
        return this.filterObject[key];
    }

    removeFilter(key: string, fetch = true): void {
        delete this.filterObject[key];
        if (fetch) {
            this.fetch();
        }
    }

    addSort(key: string, direction: SortDirection, fetch = true): void {
        this.clearSort(key, fetch);
        this.sortObjectsArray.push({key, direction});
        if (fetch) {
            this.fetch();
        }
    }

    clearSort(key: string, fetch = true): void {
        this.sortObjectsArray = this.sortObjectsArray.filter(sort => sort.key !== key);
        if (fetch) {
            this.fetch();
        }
    }

    clearAllSort(fetch = true): void {
        this.sortObjectsArray = [];
        if (fetch) {
            this.fetch();
        }
    }

    private getSortArray(): string[] {
        return this.sortObjectsArray.map(sort => `${sort.direction === 'asc' ? '' : '-'}${sort.key}`);
    }

    destroy() {
        this.sub.unsubscribe();
    }
}
