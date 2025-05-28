import { Component, EventEmitter, input, output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-confirmation-button',
  templateUrl: './confirmation-button.component.html',
  standalone: true,
  imports: [CommonModule]
})
export class ConfirmationButtonComponent {
  disabled = input<boolean>(false);
  text = input<string>('Submit');
  click = output<void>();

  onClick(): void {
    if (!this.disabled()) {
      this.click.emit();
    }
  }
}
