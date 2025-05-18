import {Component, OnInit} from '@angular/core';
import {SiteRefreshService} from './shared/services/site-refresh.service';
import {RouteConfigLoadEnd, RouteConfigLoadStart, Router} from '@angular/router';
import {ThemeModeService} from './shared/services/theme-mode.service';
import {UserWebsocketsService} from './shared/services/user-websockets.service';
import {ConfigurationsService} from './shared/services/configurations.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  loadingElement: HTMLElement;

  constructor(private siteRefreshService: SiteRefreshService,
              private router: Router,
              private themeModeService: ThemeModeService,
              private userWebsocketsService: UserWebsocketsService,
              private configurationsService: ConfigurationsService,
  ) {
    this.userWebsocketsService.connect();
    this.themeModeService.initThemeMode();
    this.siteRefreshService.registerRouter();
    this.configurationsService.loadData();
  }

  ngOnInit(): void {
    this.loadingElement = document.getElementById("loading-container");
    this.hideLoading();

    this.router.events.subscribe(event => {
      if (event instanceof RouteConfigLoadStart) {
        this.showLoading();
      } else if (event instanceof RouteConfigLoadEnd) {
        this.hideLoading();
      }
    });
  }

  private showLoading(): void {
    this.loadingElement.style.display = 'flex';
  }

  private hideLoading(): void {
    this.loadingElement.style.display = 'none';
  }
}
