import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TableExamplePageComponent} from './table-example-page/table-example-page.component';
import {RouterModule, Routes} from '@angular/router';
import {MatTableModule} from '@angular/material/table';
import {SharedModule} from '../shared/shared.module';
import {MatButtonModule} from '@angular/material/button';
import {MatMenuModule} from '@angular/material/menu';
import {MatIconModule} from '@angular/material/icon';
import {MatSortModule} from '@angular/material/sort';


const routes: Routes = [
  {path: '', component: TableExamplePageComponent, data: {routeName: 'tables'}},
];

@NgModule({
  declarations: [
    TableExamplePageComponent
  ],
    imports: [
        RouterModule.forChild(routes),
        CommonModule,
        MatTableModule,
        SharedModule,
        MatButtonModule,
        MatMenuModule,
        MatIconModule,
        MatSortModule
    ]
})
export class TableExampleModule { }
