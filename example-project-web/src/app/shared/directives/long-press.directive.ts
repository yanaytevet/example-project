import {Directive, ElementRef, EventEmitter, HostListener, Input, Output} from '@angular/core';

@Directive({
  selector: '[longPress]',
})
export class LongPressDirective {
  @Output() onLongPress = new EventEmitter<void>();
  timeoutId: NodeJS.Timeout;

  constructor(private el: ElementRef) {
  }

  @HostListener('mousedown') onMouseEnter() {
    this.timeoutId = setTimeout(() => this.executeFunc(), 500);
  }

  @HostListener('touchstart') onTouchStart() {
    this.timeoutId = setTimeout(() => this.executeFunc(), 500);
  }

  @HostListener('mouseup') onMouseLeave() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  }

  @HostListener('touchend') onTouchEnd() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  }

  executeFunc(): void {
    this.timeoutId = null;
    this.onLongPress.emit();
    navigator.vibrate(200);
  }
}
