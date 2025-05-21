import {computed, inject, Injectable, signal} from '@angular/core';
import {Router} from '@angular/router';
import {AuthSchema, authView, loginView, logoutView, UserSchema} from '../../../generated-files/auth';
import {RoutingService} from '../services/routing.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  auth = signal<AuthSchema>(null);
  user = computed<UserSchema>(() => {
    return this.auth()?.user ?? null;
  });
  isLoggedIn = computed<boolean>(() => {
    return this.auth()?.is_authenticated ?? null;
  });

  private routingService = inject(RoutingService);

  constructor() {
    void this.checkAuth();
  }

  async tryLogin(username: string, password: string) {
    const {data} = await loginView({body: {username, password}});
    this.auth.set(data);
  }

  async logout() {
    await logoutView({body: {}});
    await this.checkAuth();
    if (!this.isLoggedIn()) {
      await this.routingService.navigateToLogin();
    }
  }

  async checkAuth() {
    const res = await authView();
    this.auth.set(res.data);
  }
}
