import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {NgxPermissionsService} from 'ngx-permissions';
import {RoutingService} from './routing.service';
import {distinctUntilChanged, firstValueFrom, map, ReplaySubject} from 'rxjs';
import {AuthUser} from '../models/users/auth-user';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private readonly _authUserSub = new ReplaySubject<AuthUser>(1);
  readonly authUser$ = this._authUserSub.asObservable();
  readonly fullUser$ = this.authUser$.pipe(map(authUser => authUser?.user || null));
  readonly isAuthenticated$ = this.authUser$.pipe(map(authUser => authUser?.isAuthenticated),
    distinctUntilChanged());
  public userId: number;

  constructor(private http: HttpClient, private routingService: RoutingService,
              private permissionsService: NgxPermissionsService) {
    this.updateIsLoggedIn();
  }

  set authUser(val: AuthUser) {
    this._authUserSub.next(val);
    this.permissionsService.flushPermissions();
    this.permissionsService.loadPermissions(val?.user?.permissions || []);
    this.userId = val?.user?.id;
  }

  async updateIsLoggedIn(): Promise<void> {
    this.authUser = await firstValueFrom<AuthUser>(this.http.get<AuthUser>('/auth/', {}));
  }

  async login(username: string, password: string): Promise<AuthUser> {
    const authUser = await firstValueFrom<AuthUser>(this.http.post<AuthUser>('/auth/login/', {username, password}));
    this.authUser = authUser;
    return authUser;
  }

  async logout(): Promise<AuthUser> {
    const authUser = await firstValueFrom<AuthUser>(this.http.post<AuthUser>('/auth/logout/', {}));
    this.authUser = authUser;
    this.routingService.navigateToLogin();
    return authUser;
  }

  async changePasswords(oldPassword: string, newPassword: string): Promise<void> {
    await firstValueFrom<AuthUser>(this.http.post<AuthUser>('/auth/change-password/', {oldPassword, newPassword}));
  }
}
