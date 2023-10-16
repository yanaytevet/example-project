import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {FormExamplePageComponent} from './form-example-page/form-example-page.component';
import {RouterModule, Routes} from '@angular/router';
import {MatInputModule} from '@angular/material/input';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {SharedModule} from '../shared/shared.module';
import {MatCheckboxModule} from '@angular/material/checkbox';


const routes: Routes = [
  {path: '', component: FormExamplePageComponent, data: {routeName: 'forms'}},
];


@NgModule({
  declarations: [
    FormExamplePageComponent
  ],
    imports: [
        RouterModule.forChild(routes),
        CommonModule,
        MatInputModule,
        MatIconModule,
        MatButtonModule,
        FormsModule,
        ReactiveFormsModule,
        SharedModule,
        MatCheckboxModule
    ]
})
export class FormExampleModule { }
