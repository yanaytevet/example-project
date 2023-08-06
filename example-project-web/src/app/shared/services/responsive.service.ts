import { Injectable } from '@angular/core';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import {map, Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ResponsiveService {
  public isHandout$: Observable<boolean>;

  constructor(private responsive: BreakpointObserver) {
    this.isHandout$ = this.responsive.observe(Breakpoints.Handset).pipe(map((result => result.matches)));
  }
}
