import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {DialogsExamplePageComponent} from './dialogs-example-page/dialogs-example-page.component';
import {MatButtonModule} from '@angular/material/button';
import {RouterModule, Routes} from '@angular/router';
import {MatDialogModule} from '@angular/material/dialog';


const routes: Routes = [
  {path: '', component: DialogsExamplePageComponent, data: {routeName: 'dialogs'}},
];

@NgModule({
  declarations: [
    DialogsExamplePageComponent
  ],
  imports: [
      RouterModule.forChild(routes),
      MatDialogModule,
      CommonModule,
      MatButtonModule
  ]
})
export class DialogsExampleModule { }
