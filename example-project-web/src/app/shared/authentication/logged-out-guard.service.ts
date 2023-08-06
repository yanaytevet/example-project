import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, CanActivate, RouterStateSnapshot} from '@angular/router';
import {map, Observable} from 'rxjs';
import {RoutingService} from '../services/routing.service';
import {AuthenticationService} from '../services/authentication.service';

@Injectable()
export class LoggedOutGuard implements CanActivate {

  constructor(private routingService: RoutingService, private authService: AuthenticationService) {
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.authService.isAuthenticated$.pipe(map(isAuthenticated => {
      if (!isAuthenticated) {
        return true;
      } else {
        this.routingService.navigateToRoot();
        return false;
      }
    }));
  }
}
