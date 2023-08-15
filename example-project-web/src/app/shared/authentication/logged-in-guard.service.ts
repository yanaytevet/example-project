import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, RouterStateSnapshot} from '@angular/router';
import {map, Observable} from 'rxjs';
import {RoutingService} from '../services/routing.service';
import {AuthenticationService} from './authentication.service';

@Injectable()
export class LoggedInGuard {

  constructor(private routingService: RoutingService, private authService: AuthenticationService) {
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return this.authService.isAuthenticated$.pipe(map(isAuthenticated => {
      if (isAuthenticated) {
        return true;
      } else {
        this.routingService.navigateToLogin(state.url);
        return false;
      }
    }));
  }
}
