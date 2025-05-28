import {UrlTree} from '@angular/router';

export interface LinkItem {
  linkArr?: UrlTree;
  text: string;
  active?: boolean;
}
