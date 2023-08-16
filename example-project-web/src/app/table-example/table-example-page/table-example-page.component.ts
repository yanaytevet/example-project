import {Component, OnInit} from '@angular/core';
import {Block} from '../../shared/interfaces/blocks/block';
import {PaginationDataHandler} from '../../shared/components/pagination-tables/pagination-data-handler';
import {BooleanDisplay} from '../../shared/string-display/boolean-display';
import {BlocksApiService} from '../../shared/apis/blocks-api.service';
import {StringUtilsService} from '../../shared/services/string-utils.service';
import {ZBlockType} from '../../shared/interfaces/blocks/blocks-type';

@Component({
  selector: 'app-table-example-page',
  templateUrl: './table-example-page.component.html',
  styleUrls: ['./table-example-page.component.scss']
})
export class TableExamplePageComponent implements OnInit {
  genericDataHandler: PaginationDataHandler<Block>;
  booleanDisplay = new BooleanDisplay();

  displayedColumns: string[] = ['id', 'blockType', 'a', 'b', 'c', 'actions'];

  constructor(private blocksApiService: BlocksApiService,
              private stringUtilsService: StringUtilsService) {
    this.genericDataHandler = new PaginationDataHandler<Block>(async params => {
      return await this.blocksApiService.getBlocksPaginationList(params);
    });
  }

  ngOnInit(): void {
    this.genericDataHandler.fetch();
  }

  async createItem(): Promise<void> {
    await this.blocksApiService.postCreateBlock({
      a: this.stringUtilsService.generateRandomString(10),
      b: Math.floor(Math.random() * 11),
      c: Math.random() < 0.5,
      blockType: this.stringUtilsService.getRandomEnumValue(ZBlockType.enum),
    });
    await this.genericDataHandler.fetch();
  }

  async deleteItem(block: Block): Promise<void> {
    await this.blocksApiService.deleteBlockItemById(block.id);
    await this.genericDataHandler.fetch();
  }

  async updateItem(block: Block): Promise<void> {
    await this.blocksApiService.patchBlockItemById(block.id,{
      a: this.stringUtilsService.generateRandomString(10),
      b: Math.floor(Math.random() * 11),
      c: Math.random() < 0.5,
    });
    await this.genericDataHandler.fetch();
  }

  async buildItem(block: Block): Promise<void> {
    await this.blocksApiService.putActionsBlockItemById(block.id, {action: 'build'});
    await this.genericDataHandler.fetch();
  }
}
