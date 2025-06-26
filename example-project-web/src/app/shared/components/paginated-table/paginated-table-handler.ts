import {PaginatedData} from './paginated-data';
import {BehaviorSubject, Subscription} from 'rxjs';
import {PaginationInput} from './pagination-input';
import {computed, signal} from '@angular/core';
import {CallbacksDebouncer} from '../../data/callbacks-debouncer';
import {deleteNested, getAllNestedKeys, getNested, setNested} from '../../util-functions/nested-objects-utils';

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
    filterSignal = signal<Record<string, any>>({});
    filterKeysSignal = computed<string[]>(() => {
        return getAllNestedKeys(this.filterSignal());
    });
    dictFilterSignal = signal<Record<string, any>>({});
    dictFilterKeysSignal = computed<string[]>(() => {
        return getAllNestedKeys(this.dictFilterSignal());
    });

    sortObjectsArray: SortObject[] = [];
    fetchesDebouncer = new CallbacksDebouncer();

    private readonly _isLoadingSub = new BehaviorSubject<boolean>(true);
    readonly isLoading$ = this._isLoadingSub.asObservable();

    private readonly _paginationDataSub = new BehaviorSubject<PaginatedData<T>>(null);
    readonly paginationData$ = this._paginationDataSub.asObservable();
    readonly paginationDataSignal = signal<PaginatedData<T>>(null);
    readonly itemsSignal = computed<T[]>(() => this.paginationDataSignal()?.data || []);

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

    private updateFilterSignal(): void {
        this.filterSignal.set({...this.filterObject});
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
                    ...this.filterObject,
                    dict_filter: JSON.stringify(this.dictFilterSignal())
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
        this.updateFilterSignal();
        if (fetch) {
            this.fetch();
        }
    }

    setFilter(key: string, value: any, fetch = true): void {
        this.filterObject[key] = value;
        this.updateFilterSignal();
        if (fetch) {
            this.fetch();
        }
    }

    clearFilter(key: string, fetch = true): void {
        delete this.filterObject[key];
        this.updateFilterSignal();
        if (fetch) {
            this.fetch();
        }
    }

    getFilterValue(key: string): any {
        return this.filterObject[key];
    }

    hasFilterValue(key: string): boolean {
        return key in this.filterObject;
    }

    clearAllDictFilter(fetch = true): void {
        this.dictFilterSignal.set({});
        if (fetch) {
            this.fetch();
        }
    }

    setDictFilter(key: string, value: any, fetch = true): void {
        const currentDictFilters = structuredClone(this.dictFilterSignal());
        setNested(currentDictFilters, key, value);
        this.dictFilterSignal.set(currentDictFilters);
        if (fetch) {
            this.fetch();
        }
    }

    clearDictFilter(key: string, fetch = true): void {
        const currentDictFilters = structuredClone(this.dictFilterSignal());
        deleteNested(currentDictFilters, key);
        this.dictFilterSignal.set(currentDictFilters);
        if (fetch) {
            this.fetch();
        }
    }

    getDictFilterValue(key: string): any {
        return getNested(this.dictFilterSignal(), key);
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

    async updateValues(updatedItems: T[]) {
        this.paginationData = {...this.paginationData, data: updatedItems};
    }
}
