import {ApplicationConfig, inject, provideAppInitializer, provideZoneChangeDetection} from '@angular/core';
import {provideRouter} from '@angular/router';
import {provideIcons} from '@ng-icons/core';
import {
    featherFile, featherGrid, featherMessageSquare, featherZap,
    featherChevronRight, featherChevronDown, featherLogOut
} from '@ng-icons/feather-icons';

import {routes} from './app.routes';
import {ApiConfigService} from './shared/api/api-config.service';
import {AuthenticationService} from './shared/authentication/authentication.service';

export const appConfig: ApplicationConfig = {
    providers: [
        provideZoneChangeDetection({eventCoalescing: true}),
        provideRouter(routes),
        provideAppInitializer(() => {
            const apiConfigService = inject(ApiConfigService);
            return apiConfigService.initialize();
        }),
        provideAppInitializer(() => {
            const authenticationService = inject(AuthenticationService);
        })
    ]
};
