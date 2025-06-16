import {ApplicationConfig, inject, provideAppInitializer, provideZoneChangeDetection} from '@angular/core';
import {provideRouter} from '@angular/router';

import {routes} from './app.routes';
import {ApiConfigService} from './shared/api/api-config.service';
import {AuthenticationService} from './shared/authentication/authentication.service';
import {DarkModeService} from './shared/services/dark-mode.service';

export const appConfig: ApplicationConfig = {
    providers: [
        provideZoneChangeDetection({eventCoalescing: true}),
        provideRouter(routes),
        provideAppInitializer(() => {
            const apiConfigService = inject(ApiConfigService);
            return apiConfigService.initialize();
        }),
        provideAppInitializer(() => {
            inject(AuthenticationService);
        }),
        provideAppInitializer(() => {
            inject(DarkModeService);
        })
    ]
};
