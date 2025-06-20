import {computed, inject, Injectable, signal} from '@angular/core';
import {AuthSchema, authView, loginView, logoutView, UserSchema} from '../../../generated-files/auth';
import {RoutingService} from '../services/routing.service';
import {toObservable} from '@angular/core/rxjs-interop';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  auth = signal<AuthSchema>(null);
  auth$ = toObservable(this.auth);
  user = computed<UserSchema>(() => {
    return this.auth()?.user ?? null;
  });
  isLoggedIn = computed<boolean>(() => {
    return this.auth()?.is_authenticated ?? null;
  });
  userInitials = computed<string>(() => {
    return this.user()?.initials?.toUpperCase() ?? null;
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
