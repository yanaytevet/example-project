import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

export interface KeyValue {
    key: string;
    value: string;
}

export interface KeyValueDialogData {
    title: string;
    text: string;
    cancelActionName?: string;
    confirmActionName?: string;
    allowEmpty?: boolean;
    allowEmptyValues?: boolean;
    defaultValue?: Record<string, string>;
}

@Component({
    selector: 'app-key-value-dialog',
    templateUrl: './key-value-dialog.component.html',
    styleUrls: ['./key-value-dialog.component.scss']
})
export class KeyValueDialogComponent implements OnInit {
    title = '';
    text = '';
    allowEmpty: boolean = false;
    allowEmptyValues: boolean = false;
    cancelActionName = 'Cancel';
    confirmActionName = 'Confirm';
    isValid = false;
    keyValues: KeyValue[] = [];

    constructor(
        @Inject(MAT_DIALOG_DATA) public data: KeyValueDialogData,
        public dialogRef: MatDialogRef<KeyValueDialogComponent>,
    ) {
        this.title = data.title;
        this.text = data.text;
        if (this.data.cancelActionName) {
            this.cancelActionName = this.data.cancelActionName;
        }
        if (this.data.confirmActionName) {
            this.confirmActionName = this.data.confirmActionName;
        }
        if (this.data.allowEmpty) {
            this.allowEmpty = this.data.allowEmpty;
        }
        if (this.data.allowEmptyValues) {
            this.allowEmptyValues = this.data.allowEmptyValues;
        }
        if (this.data.defaultValue) {
            this.keyValues = [];
            Object.keys(this.data.defaultValue).forEach(key => {
                this.keyValues.push({key, value: this.data.defaultValue[key]});
            });
        }

        this.calcIsValid();
    }

    calcIsValid(): void {
        if (this.keyValues.some(keyValue => keyValue.key.length === 0)) {
            this.isValid = false;
            return;
        }

        if (this.allowEmpty) {
            this.isValid = true;
            return;
        }

        if (this.keyValues.length === 0) {
            this.isValid = false;
            return;
        }

        if (this.allowEmptyValues) {
            this.isValid = true;
            return;
        }

        const keysSet = new Set<string>();
        this.keyValues.forEach(keyValue => {
            if (keyValue.value.length === 0) {
                this.isValid = false;
                return;
            }
            if (keysSet.has(keyValue.key)) {
                this.isValid = false;
                return;
            }
            keysSet.add(keyValue.key);
        });
        this.isValid = true;
    }

    ngOnInit(): void {
    }

    submit(): void {
        if (!this.isValid) {
            return;
        }
        const res: Record<string, string> = {}
        this.keyValues.forEach(keyValue => {
            res[keyValue.key] = keyValue.value;
        });
        this.dialogRef.close(res);
    }

    addKeyValue(): void {
        this.keyValues.push({key: '', value: ''});
    }
}
