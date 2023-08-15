import {Injectable} from '@angular/core';
import {BehaviorSubject} from "rxjs";
import {Themes} from "../enums/theme-options";

@Injectable({
  providedIn: 'root'
})
export class ThemeModeService {
  private readonly _themeModeSub = new BehaviorSubject<Themes>(null);
  readonly themeMode$ = this._themeModeSub.asObservable();
  private prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');

  initThemeMode() {
    this.prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
    const usedTheme = localStorage.getItem('theme');
    this.themeMode = usedTheme ? usedTheme as Themes : Themes.SYSTEM;
    this.prefersDarkMode.addEventListener('change', this.onPrefersDarkModeChange.bind(this));
  }

  onPrefersDarkModeChange(event: MediaQueryListEvent) {
    const usedTheme = localStorage.getItem('theme');
    if(this.themeMode === Themes.SYSTEM || usedTheme === Themes.SYSTEM) {
      this.themeMode = event.matches ? Themes.DARK : Themes.LIGHT;
    }
  }

  switchThemeMode(theme: Themes) {
    this.themeMode = theme;
    localStorage.setItem('theme', theme);
  }

  public get themeMode(): Themes {
    return this._themeModeSub.getValue();
  }
  public set themeMode(val: Themes) {
    if (val === this.themeMode) {
      return
    }
    let valueToSet = val;
    if(val === Themes.SYSTEM) {
      this.prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');
      valueToSet = this.prefersDarkMode.matches ? Themes.DARK : Themes.LIGHT;
    }

    document.documentElement.classList.remove(Themes.DARK, Themes.LIGHT, Themes.SYSTEM);
    document.documentElement.classList.add(valueToSet)
    this._themeModeSub.next(val);
  }
}
