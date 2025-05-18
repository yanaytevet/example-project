import {Injectable} from '@angular/core';
import {NgxPermissionsService} from 'ngx-permissions';
import {distinctUntilChanged, map, ReplaySubject} from 'rxjs';
import {AuthUser, ZAuthUser} from '../interfaces/users/auth-user';
import {RoutingService} from '../services/routing.service';
import {BaseApiService} from '../services/base-api.service';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private readonly _authUserSub = new ReplaySubject<AuthUser>(1);
  readonly authUser$ = this._authUserSub.asObservable();
  readonly user$ = this.authUser$.pipe(map(authUser => authUser?.user || null));
  readonly isAuthenticated$ = this.authUser$.pipe(map(authUser => authUser?.is_authenticated),
    distinctUntilChanged());
  public userId: number;
  private _authUser: AuthUser;

  constructor(private baseApi: BaseApiService, private routingService: RoutingService,
              private permissionsService: NgxPermissionsService) {
    this.updateIsLoggedIn();
  }

  set authUser(val: AuthUser) {
    this._authUserSub.next(val);
    this.permissionsService.flushPermissions();
    this.permissionsService.loadPermissions(val?.user?.permissions || []);
    this.userId = val?.user?.id;
    this._authUser = val;
  }

  get authUser(): AuthUser {
    return this._authUser;
  }

  async updateIsLoggedIn(): Promise<void> {
    this.authUser = await this.baseApi.get<AuthUser>(ZAuthUser, '/auth/', {});
  }

  async login(username: string, password: string): Promise<AuthUser> {
    const authUser: AuthUser = await this.baseApi.post<AuthUser>(ZAuthUser, '/auth/login/', {username, password});
    this.authUser = authUser;
    return authUser;
  }

  async logout(): Promise<AuthUser> {
    const authUser: AuthUser = await this.baseApi.post<AuthUser>(ZAuthUser, '/auth/logout/', {});
    this.authUser = authUser;
    this.routingService.navigateToLogin();
    return authUser;
  }

  async changePasswords(oldPassword: string, newPassword: string): Promise<void> {
    await this.baseApi.post<AuthUser>(ZAuthUser, '/auth/change-password/', {oldPassword, newPassword});
  }
}
