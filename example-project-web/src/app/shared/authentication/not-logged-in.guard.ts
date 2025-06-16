import {CanActivateFn} from '@angular/router';
import {inject} from '@angular/core';
import {AuthenticationService} from './authentication.service';
import {filter, firstValueFrom} from 'rxjs';
import {toObservable} from '@angular/core/rxjs-interop';
import {RoutingService} from '../services/routing.service';

export const notLoggedInGuard: CanActivateFn = () => {
    const authService = inject(AuthenticationService);
    const routingService = inject(RoutingService);

    const obs = toObservable(authService.isLoggedIn).pipe(
        filter((val): val is boolean => val !== null)
    );

    return firstValueFrom(obs).then(isLoggedIn => {
        return !isLoggedIn ? true : routingService.getRootUrl();
    });
};
