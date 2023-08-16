import {Component, Input, OnInit} from '@angular/core';
import {PaginationDataHandler} from '../pagination-data-handler';
import {PageEvent} from '@angular/material/paginator';
import {NumberInputDialogComponent} from '../../../dialogs/number-input-dialog/number-input-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {
  ListSingleSelectionDialogComponent
} from '../../../dialogs/list-single-selection-dialog/list-single-selection-dialog.component';

@Component({
  selector: 'app-paginator',
  templateUrl: './paginator.component.html',
  styleUrls: ['./paginator.component.scss']
})
export class PaginatorComponent implements OnInit {
  @Input() genericDataHandler: PaginationDataHandler<any>;
  possiblePageSizes: number[] = [25, 50 ,100];

  constructor(private dialog: MatDialog) { }

  ngOnInit(): void {
  }

  setPageData(event: PageEvent): void {
    this.genericDataHandler.fetchPage(event.pageIndex, event.pageSize)
  }

  get currentItemsText(): string {
    const paginationData = this.genericDataHandler?.paginationData;
    if (!paginationData) {
      return '';
    }
    if (paginationData.totalAmount === 0) {
      return 'item 0 of 0';
    }
    const start = 1 + paginationData.page * paginationData.pageSize;
    const end = Math.min(start + paginationData.pageSize - 1, paginationData.totalAmount);
    if (start === end) {
      return `item ${start} of ${paginationData.totalAmount}`
    }
    return `items ${start} - ${end} of ${paginationData.totalAmount}`
  }

  goBackOnePage() {
    this.genericDataHandler.currentPage -= 1;
    this.genericDataHandler.fetch();
  }

  goForwardOnePage() {
    this.genericDataHandler.currentPage += 1;
    this.genericDataHandler.fetch();
  }

  async openSelectPageDialog(): Promise<void> {
    const dialogRef = this.dialog.open(NumberInputDialogComponent, {
      data: {
        title: 'Select Page',
        text: `Set the page number. Acceptable values are numbers between 1 and ${this.genericDataHandler.paginationData?.pagesAmount}.`,
        label: 'Page',
        defaultValue: this.genericDataHandler.paginationData?.page + 1,
        confirmActionName: 'Update',
      },
      width: '400px',
    });

    const newPage = await dialogRef.afterClosed().toPromise();
    if (newPage !== undefined) {
      this.genericDataHandler.currentPage = newPage - 1;
      await this.genericDataHandler.fetch();
    }
  }

  async openSelectPageSizeDialog(): Promise<void> {
    const dialogRef = this.dialog.open(ListSingleSelectionDialogComponent, {
      data: {
        title: 'Select Page Size',
        text: `Select the number of items per page.`,
        confirmActionName: 'Update',
        label: 'Page Size',
        defaultValue: this.genericDataHandler.pageSize,
        options: [
          {display:'25', value: 25},
          {display:'50', value: 50},
          {display:'100', value: 100},
        ],
      }
    });

    const newPageSize: number = await dialogRef.afterClosed().toPromise();
    if (newPageSize) {
      this.genericDataHandler.pageSize = newPageSize;
      await this.genericDataHandler.fetch();
    }
  }
}
