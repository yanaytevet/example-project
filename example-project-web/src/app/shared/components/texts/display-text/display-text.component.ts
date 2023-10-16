import {Component, Input} from '@angular/core';

@Component({
    selector: 'app-display-text',
    templateUrl: './display-text.component.html',
    styleUrls: ['./display-text.component.scss']
})
export class DisplayTextComponent {
    _text: string = '';
    @Input() set text(val: string) {
        this._text = val;
        this.updateFormattedText();
    }

    get text(): string {
        return this._text;
    }

    formattedText: string = '';


    private updateFormattedText() {
        this.formattedText = this.text
            .replace(/\*\*(.*)\*\*/gim, '<b>$1</b>') // bold text
            .replace(/\_\_(.*)\_\_/gim, '<u>$1</u>'); // italic text
    }
}
