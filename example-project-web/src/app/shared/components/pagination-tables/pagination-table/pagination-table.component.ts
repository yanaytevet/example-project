import {
  AfterContentInit,
  Component,
  ContentChildren,
  Input,
  OnDestroy,
  OnInit,
  QueryList,
  ViewChild,
  ViewEncapsulation
} from '@angular/core';
import {PaginationDataHandler} from '../pagination-data-handler';
import {MatColumnDef, MatTable, MatTableDataSource} from '@angular/material/table';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-pagination-table',
  templateUrl: './pagination-table.component.html',
  styleUrls: ['./pagination-table.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PaginationTableComponent<T> implements OnInit, OnDestroy, AfterContentInit {
  @Input() paginationDataHandler: PaginationDataHandler<T>;
  @Input() displayedColumns: string[] = [];
  @Input() rowToClassCallback: (obj: T) => string = null;
  @ViewChild(MatTable, { static: true }) table: MatTable<T>;
  @ContentChildren(MatColumnDef) columnDefs: QueryList<MatColumnDef>;
  dataSource: MatTableDataSource<T> = null;

  paginationDataSub: Subscription;

  constructor() {
    this.dataSource = new MatTableDataSource<T>([]);
  }

  ngOnInit(): void {
    this.paginationDataSub = this.paginationDataHandler.paginationData$.subscribe(paginationData => {
      if (paginationData) {
        this.dataSource.data = paginationData.data;
      }
    })
  }

  ngAfterContentInit() {
    this.columnDefs.forEach(columnDef => this.table.addColumnDef(columnDef));
  }

  ngOnDestroy(): void {
    this.paginationDataSub.unsubscribe();
  }
}
