import {PaginationData} from './pagination-data';
import {BehaviorSubject} from 'rxjs';

export class PaginationDataHandler<T> {
  currentPage: number = 0;
  pageSize: number = 25;
  isEmpty: boolean = true;
  filterObject: Record<string, any> = {};
  sortOrder: string[] = [];

  private readonly _paginationDataSub = new BehaviorSubject<PaginationData<T>>(null);
  readonly paginationData$ = this._paginationDataSub.asObservable();
  private autoFetchInterval: number;

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
    this.currentPage = Math.min(this.currentPage, this.paginationData?.pagesAmount - 1 || 0);
    this.currentPage = Math.max(this.currentPage, 0);
    const data = {
      page: this.currentPage,
      page_size: this.pageSize,
      order_by: this.getSortString(),
      ...this.filterObject,
    }
    this.paginationData = await this.fetchPaginationData(data);
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

  getFilterValue(key: string): any {
    return this.filterObject[key];
  }

  removeFilter(key: string, value: string): void {
    this.filterObject[key] = value;
    this.fetch();
  }

  addSort(key: string): void {
    this.sortOrder.push(key);
    this.fetch();
  }

  clearSort(key: string): void {
    this.sortOrder = [];
    this.fetch();
  }

  private getSortString(): string {
    return this.sortOrder.join(',');
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
}
