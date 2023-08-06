import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot} from '@angular/router';
import {map, Observable} from 'rxjs';
import {RoutingService} from '../services/routing.service';
import {AuthenticationService} from '../services/authentication.service';
import {NgxPermissionsService} from 'ngx-permissions';

@Injectable()
export abstract class PermissionsGuard implements CanActivate {

  protected constructor(private ngxPermissionsService: NgxPermissionsService, private authService: AuthenticationService) {
  }

  abstract checkPermissions(): boolean;

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.authService.isAuthenticated$.pipe(map(isAuthenticated => {
      return isAuthenticated && this.checkPermissions();
    }));
  }
}
