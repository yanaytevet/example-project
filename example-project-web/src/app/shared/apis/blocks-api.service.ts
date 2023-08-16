import {Injectable} from '@angular/core';
import {BaseApiService} from '../services/base-api.service';
import {Block, ZBlock} from '../interfaces/blocks/block';
import {PaginationData} from '../components/pagination-tables/pagination-data';

@Injectable({
  providedIn: 'root'
})
export class BlocksApiService {
  constructor(private baseApi: BaseApiService) {
  }

  async sendBlockEvent(eventType: string): Promise<void> {
    await this.baseApi.post<void>(null, '/api/blocks/websocket-test/', {eventType});
  }

  async getBlockItemById(id: number): Promise<Block> {
    return await this.baseApi.get<Block>(ZBlock, `/api/blocks/${id}/`, {});
  }

  async patchBlockItemById(id: number, data: any): Promise<Block> {
    return await this.baseApi.patch<Block>(ZBlock, `/api/blocks/${id}/`, data);
  }

  async putActionsBlockItemById(id: number, data: any): Promise<Block> {
    return await this.baseApi.put<Block>(ZBlock, `/api/blocks/${id}/`, data);
  }

  async deleteBlockItemById(id: number): Promise<void> {
    await this.baseApi.delete( `/api/blocks/${id}/`);
  }

  async getBlocksPaginationList(params: any): Promise<PaginationData<Block>> {
    return await this.baseApi.get<PaginationData<Block>>(null, `/api/blocks/`, params);
  }

  async postCreateBlock(data: any): Promise<Block> {
    return await this.baseApi.post<Block>(ZBlock, `/api/blocks/`, data);
  }
}
