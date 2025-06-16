import {Directive, inject, output} from '@angular/core';
import {DIALOG_DATA} from './dialogs.service';

@Directive()
export abstract class BaseDialogComponent<TInput = void, TOutput = void> {
    data: TInput = inject(DIALOG_DATA);
    closeDialog = output<TOutput | null>();

    // Method to emit the result and close the dialog
    public emitClose(result: TOutput | null = null): void {
        this.closeDialog.emit(result);
    }
}
