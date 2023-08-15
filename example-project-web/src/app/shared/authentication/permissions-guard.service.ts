import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, RouterStateSnapshot} from '@angular/router';
import {map, Observable} from 'rxjs';
import {AuthenticationService} from './authentication.service';
import {AuthUser} from '../interfaces/users/auth-user';

@Injectable()
export abstract class PermissionsGuard {

  constructor(private authService: AuthenticationService) {
  }

  abstract checkPermissions(authUser: AuthUser): boolean;

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.authService.authUser$.pipe(map(authUser => {
      return authUser.isAuthenticated && this.checkPermissions(authUser);
    }));
  }
}
