import { Injectable } from '@angular/core';
import {client as authClient} from '../../../generated-files/auth/client.gen';
import {client as api_usersClient} from '../../../generated-files/api/users/client.gen';
import {client as api_configurationsClient} from '../../../generated-files/api/configurations/client.gen';
import {client as api_blocksClient} from '../../../generated-files/api/blocks/client.gen';

@Injectable({
  providedIn: 'root'
})
export class ApiConfigService {
  readonly clients = [authClient, api_usersClient, api_configurationsClient, api_blocksClient];

  initialize(): void {
    this.clients.forEach((client) => {
      client.setConfig({
        baseUrl: 'http://localhost:8000/',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });
    });
  }
}
