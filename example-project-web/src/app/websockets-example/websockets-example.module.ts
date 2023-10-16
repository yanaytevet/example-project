import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WebsocketsExamplePageComponent } from './websockets-example-page/websockets-example-page.component';
import {RouterModule, Routes} from '@angular/router';
import {MatButtonModule} from '@angular/material/button';
import {SharedModule} from '../shared/shared.module';

const routes: Routes = [
  {path: '', component: WebsocketsExamplePageComponent, data: {routeName: 'websockets'}},
];

@NgModule({
  declarations: [
    WebsocketsExamplePageComponent
  ],
    imports: [
        RouterModule.forChild(routes),
        CommonModule,
        MatButtonModule,
        SharedModule
    ]
})
export class WebsocketsExampleModule { }
