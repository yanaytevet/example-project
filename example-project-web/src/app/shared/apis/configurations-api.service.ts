import {Injectable} from '@angular/core';
import {BaseApiService} from '../services/base-api.service';
import {FullConfigurations} from '../interfaces/configurations/full-configurations';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationsApiService {
  constructor(private baseApi: BaseApiService) {
  }

  async getConfigurations(): Promise<FullConfigurations> {
    return await this.baseApi.get<FullConfigurations>(null, '/api/configurations/');
  }
}
