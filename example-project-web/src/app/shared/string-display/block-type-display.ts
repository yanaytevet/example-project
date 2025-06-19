import {EnumDisplay} from './enum-display';

export class BlockTypeDisplay extends EnumDisplay {
  override data: Record<string, string> = {
    round: 'Round',
    square: 'Square',
    triangle: 'Triangle',
  };
}
