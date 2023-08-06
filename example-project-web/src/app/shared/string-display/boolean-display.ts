import {EnumDisplay} from './enum-display';

export class BooleanDisplay extends EnumDisplay {
  override data: Record<string, string> = {
    true: 'Yes',
    false: 'No',
  };
}
