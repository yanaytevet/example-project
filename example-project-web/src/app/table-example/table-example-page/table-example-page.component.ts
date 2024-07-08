import {Component, OnInit} from '@angular/core';
import {Block} from '../../shared/interfaces/blocks/block';
import {PaginationDataHandler} from '../../shared/components/pagination-tables/pagination-data-handler';
import {BooleanDisplay} from '../../shared/string-display/boolean-display';
import {BlocksApiService} from '../../shared/apis/blocks-api.service';
import {StringUtilsService} from '../../shared/services/string-utils.service';
import {ZBlockType} from '../../shared/interfaces/blocks/blocks-type';
import {BlockTypeDisplay} from '../../shared/string-display/block-type-display';
import {BreadcrumbsService} from '../../shared/components/breadcrumbs/breadcrumbs.service';
import {BasePageComponent} from '../../shared/components/base-page-component';

@Component({
  selector: 'app-table-example-page',
  templateUrl: './table-example-page.component.html',
  styleUrls: ['./table-example-page.component.scss']
})
export class TableExamplePageComponent extends BasePageComponent implements OnInit {
  paginationDataHandler: PaginationDataHandler<Block>;
  booleanDisplay = new BooleanDisplay();
  blockTypeDisplay = new BlockTypeDisplay();

  displayedColumns: string[] = ['id', 'blockType', 'a', 'b', 'c', 'actions'];

  constructor(private blocksApiService: BlocksApiService,
              private stringUtilsService: StringUtilsService,
              private breadcrumbsService: BreadcrumbsService) {
    super();
    this.paginationDataHandler = new PaginationDataHandler<Block>(async params => {
      return await this.blocksApiService.getBlocksPaginationList(params);
    });
    this.breadcrumbs = this.breadcrumbsService.getSimpleBreadcrumbs('Table Example');
  }

  ngOnInit(): void {
    this.paginationDataHandler.fetch();
  }

  async createItem(): Promise<void> {
    await this.blocksApiService.postCreateBlock({
      a: this.stringUtilsService.generateRandomString(10),
      b: Math.floor(Math.random() * 11),
      c: Math.random() < 0.5,
      blockType: this.stringUtilsService.getRandomEnumValue(ZBlockType.enum),
    });
    await this.paginationDataHandler.fetch();
  }

  async deleteItem(block: Block): Promise<void> {
    await this.blocksApiService.deleteBlockItemById(block.id);
    await this.paginationDataHandler.fetch();
  }

  async updateItem(block: Block): Promise<void> {
    await this.blocksApiService.patchBlockItemById(block.id,{
      a: this.stringUtilsService.generateRandomString(10),
      b: Math.floor(Math.random() * 11),
      c: Math.random() < 0.5,
    });
    await this.paginationDataHandler.fetch();
  }

  async buildItem(block: Block): Promise<void> {
    await this.blocksApiService.postActionBuildBlockItemById(block.id, {shouldBuild: true});
    await this.paginationDataHandler.fetch();
  }

  rowToClassCallback = (block: Block) => {
    if (block.blockType === ZBlockType.enum.triangle) {
      return 'warning-row';
    }
    return '';
  }
}
