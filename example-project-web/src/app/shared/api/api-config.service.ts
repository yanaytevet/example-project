import { Injectable } from '@angular/core';
import {client as authClient} from '../../../generated-files/auth/client.gen';

@Injectable({
  providedIn: 'root'
})
export class ApiConfigService {
  readonly clients = [authClient];

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
