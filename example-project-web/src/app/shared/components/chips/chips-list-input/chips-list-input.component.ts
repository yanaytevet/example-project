import {Component, EventEmitter, Input, Output} from '@angular/core';
import {MatChipEditedEvent, MatChipInputEvent} from '@angular/material/chips';
import {CdkDragDrop, moveItemInArray} from '@angular/cdk/drag-drop';
import {Option} from '../../../interfaces/util/option';

@Component({
  selector: 'app-chips-list-input',
  templateUrl: './chips-list-input.component.html',
  styleUrls: ['./chips-list-input.component.scss']
})
export class ChipsListInputComponent {
  currentChips: string[] = [];

  @Input() set value(val: string[]) {
    this.currentChips = val;
    if (!this.currentChips) {
      this.currentChips = [];
    }
  }
  @Input() canEdit = false;
  @Input() label = '';

  @Output() valueChange = new EventEmitter<string[]>();


  addChip(event: MatChipInputEvent): void {
    if (!this.canEdit) {
      return;
    }
    const value = (event.value || '').trim();

    // Add our fruit
    if (value) {
      this.currentChips.push(value);
      this.valueChange.emit(this.currentChips);
    }

    // Clear the input value
    event.chipInput!.clear();
  }

  removeChip(tag: string): void {
    if (!this.canEdit) {
      return;
    }
    const index = this.currentChips.indexOf(tag);

    if (index >= 0) {
      this.currentChips.splice(index, 1);
      this.valueChange.emit(this.currentChips);
    }
  }

  editChip(tag: string, event: MatChipEditedEvent) {
    if (!this.canEdit) {
      return;
    }
    const value = event.value.trim();

    // Remove tag if it no longer has a name
    if (!value) {
      this.removeChip(tag);
      return;
    }

    // Edit existing tag
    const index = this.currentChips.indexOf(tag);
    if (index >= 0) {
      this.currentChips[index] = value;
      this.valueChange.emit(this.currentChips);
    }
  }

  drop(event: CdkDragDrop<Option[]>) {
    if (!this.canEdit) {
      return;
    }
    moveItemInArray(this.currentChips, event.previousIndex, event.currentIndex);
    this.valueChange.emit(this.currentChips);
  }

}
