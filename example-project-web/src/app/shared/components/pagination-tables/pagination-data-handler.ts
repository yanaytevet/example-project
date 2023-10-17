import {PaginationData} from './pagination-data';
import {BehaviorSubject} from 'rxjs';
import {Sort} from '@angular/material/sort';

type SortDirection = 'asc' | 'desc';

interface SortObject {
  direction: SortDirection;
  key: string;
}

export class PaginationDataHandler<T> {
  currentPage: number = 0;
  pageSize: number = 25;
  isEmpty: boolean = true;
  filterObject: Record<string, any> = {};
  sortObjectsArray: SortObject[] = [];

  private readonly _isLoadingSub = new BehaviorSubject<boolean>(true);
  readonly isLoading$ = this._isLoadingSub.asObservable();

  private readonly _paginationDataSub = new BehaviorSubject<PaginationData<T>>(null);
  readonly paginationData$ = this._paginationDataSub.asObservable();
  private autoFetchInterval: number;

  public get isLoading(): boolean {
    return this._isLoadingSub.getValue();
  }
  public set isLoading(val: boolean) {
    this._isLoadingSub.next(val);
  }

  public get paginationData(): PaginationData<T> {
    return this._paginationDataSub.getValue();
  }
  public set paginationData(val: PaginationData<T>) {
    this._paginationDataSub.next(val);
    this.isEmpty = val.pageSize === 0 && val.pagesAmount === 0;
  }

  constructor(
    private fetchPaginationData: (params: any) => Promise<PaginationData<T>>,
  ) {
  }

  public async fetch(): Promise<void> {
    this.isLoading = true;
    this.currentPage = Math.min(this.currentPage, this.paginationData?.pagesAmount - 1 || 0);
    this.currentPage = Math.max(this.currentPage, 0);
    const data = {
      page: this.currentPage,
      page_size: this.pageSize,
      order_by: this.getSortString(),
      filter: this.getFilterString(),
    }
    this.paginationData = await this.fetchPaginationData(data);
    this.isLoading = false;
  }

  public fetchPage(page: number, pageSize: number): void {
    this.currentPage = page;
    this.pageSize = pageSize;
    this.fetch();
  }

  clearAllFilter(): void {
    this.filterObject = {};
    this.fetch();
  }

  setFilter(key: string, value: any, fetch: boolean = true): void {
    this.filterObject[key] = value;
    if (fetch) {
      this.fetch();
    }
  }

  clearFilter(key: string, fetch: boolean = true): void {
    delete this.filterObject[key];
    if (fetch) {
      this.fetch();
    }
  }

  getFilterValue(key: string): any {
    return this.filterObject[key];
  }

  removeFilter(key: string, value: string): void {
    this.filterObject[key] = value;
    this.fetch();
  }

  addSort(key: string, direction: SortDirection): void {
    const currentSort = this.sortObjectsArray.find(sort => sort.key === key);
    if (currentSort) {
      currentSort.direction = direction;
    }
    else {
      this.sortObjectsArray.push({key, direction});
    }
    this.fetch();
  }

  clearSort(key: string): void {
    this.sortObjectsArray= this.sortObjectsArray.filter(sort => sort.key !== key);
    this.fetch();
  }

  private getSortString(): string {
    return JSON.stringify(this.sortObjectsArray.map(sort => `${sort.direction === 'asc' ? '' : '-'}${sort.key}`));
  }

  private getFilterString(): string {
    return JSON.stringify(this.filterObject);
  }

  startAutoFetch(seconds: number): void {
    this.clearAutoFetch();
    this.autoFetchInterval = setInterval(() => {
      this.fetch();
    }, seconds * 1000);
  }

  clearAutoFetch(): void {
    if (this.autoFetchInterval) {
      clearInterval(this.autoFetchInterval);
    }
    this.autoFetchInterval = null;
  }

  sortFromTable(sort: Sort): void {
    if (sort.direction === '') {
      this.clearSort(sort.active);
    } else if (sort.direction === 'asc' || sort.direction === 'desc') {
      this.addSort(sort.active, sort.direction);
    }
  }
}
