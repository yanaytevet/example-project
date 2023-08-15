import {Injectable} from '@angular/core';
import {BaseApiService} from '../services/base-api.service';

@Injectable({
  providedIn: 'root'
})
export class BlocksApiService {
  constructor(private baseApi: BaseApiService) {
  }

  async sendBlockEvent(eventType: string): Promise<void> {
    await this.baseApi.post<void>(null, '/api/blocks/', {eventType});
  }
}
