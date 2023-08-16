export interface PaginationData<T> {
  totalAmount: number;
  pagesAmount: number;
  page: number;
  pageSize: number;
  data: T[];
}
