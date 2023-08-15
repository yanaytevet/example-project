import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardLayoutComponent } from './dashboard-layout/dashboard-layout.component';
import {RouterOutlet} from '@angular/router';
import { HomePageComponent } from './home-page/home-page.component';
import {MatMenuModule} from '@angular/material/menu';
import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';



@NgModule({
  declarations: [
    DashboardLayoutComponent,
    HomePageComponent
  ],
  imports: [
    CommonModule,
    RouterOutlet,
    MatMenuModule,
    MatIconModule,
    MatButtonModule
  ]
})
export class HomeModule { }
