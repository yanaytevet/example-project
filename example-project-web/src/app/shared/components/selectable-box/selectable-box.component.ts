import {Component, EventEmitter, input} from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgIcon } from '@ng-icons/core';
import {bootstrapBell, bootstrapCheck} from '@ng-icons/bootstrap-icons';

@Component({
  selector: 'app-selectable-box',
  templateUrl: './selectable-box.component.html',
  styleUrls: ['./selectable-box.component.css'],
  standalone: true,
  imports: [CommonModule, NgIcon]
})
export class SelectableBoxComponent {
  // Input properties
  isSelected = input<boolean>(false);
  text =  input<string>();

  // Output property
  clicked = new EventEmitter<void>();

  protected readonly checkIcon = bootstrapCheck;

  onClick(): void {
    this.clicked.emit();
  }
}
