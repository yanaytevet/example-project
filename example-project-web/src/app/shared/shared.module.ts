import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {VarDirective} from './directives/ng-var.directive';



@NgModule({
  declarations: [
    VarDirective
  ],
  imports: [
    CommonModule
  ]
})
export class SharedModule { }
