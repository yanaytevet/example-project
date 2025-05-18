import {inject, Injectable, signal} from '@angular/core';
import {ConfigurationsApiService} from '../apis/configurations-api.service';
import {FullConfigurations} from '../interfaces/configurations/full-configurations';

@Injectable({
  providedIn: 'root'
})
export class ConfigurationsService {
  configurationsApiService = inject(ConfigurationsApiService);

  fullConfigurations = signal<FullConfigurations>(null);

  constructor() {
  }

  public async loadData(){
    const conf = await this.configurationsApiService.getConfigurations();
    this.fullConfigurations.set(conf);
  }
}
