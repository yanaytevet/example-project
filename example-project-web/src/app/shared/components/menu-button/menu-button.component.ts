import {Component, input} from '@angular/core';
import {CdkMenuModule} from '@angular/cdk/menu';
import {Action} from '../../interfaces/util/action';
import {NgIcon} from '@ng-icons/core';

@Component({
  selector: 'app-menu-button',
  imports: [
    CdkMenuModule,
    NgIcon,
  ],
  templateUrl: './menu-button.component.html',
  styleUrl: './menu-button.component.css'
})
export class MenuButtonComponent {
  text = input<string>('');
  icon = input<string>(null);
  actions= input<Action[]>();
}
