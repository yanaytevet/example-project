import {Injectable} from '@angular/core';
import {firstValueFrom} from 'rxjs';
import {ConfirmationDialogComponent} from '../dialogs/confirmation-dialog/confirmation-dialog.component';
import {DataVisibility} from '../models/npcs/data-visibility';
import {NewNpcDialogComponent} from '../dialogs/new-npc-dialog/new-npc-dialog.component';
import {NumberInputDialogComponent} from '../dialogs/number-input-dialog/number-input-dialog.component';
import {PoolDataDialogComponent, PoolDataDialogResult} from '../dialogs/pool-data-dialog/pool-data-dialog.component';
import {TextInputDialogComponent} from '../dialogs/text-input-dialog/text-input-dialog.component';
import {StatusEffectTemplate} from '../models/status-effects/status-effect-template';
import {
  StatusEffectDataDialogComponent
} from '../dialogs/status-effect-data-dialog/status-effect-data-dialog.component';
import {Pool} from '../models/pools/pool';
import {XpSpendDialogComponent, XpSpendDialogResult} from '../dialogs/xp-spend-dialog/xp-spend-dialog.component';
import {XpGainedDialogComponent, XpGainedDialogResult} from '../dialogs/xp-gained-dialog/xp-gained-dialog.component';
import {ShortCharacter} from '../models/characters/short-character';
import {
  StylesListSingleSelectionDialogComponent
} from '../dialogs/styles-list-single-selection-dialog/styles-list-single-selection-dialog.component';
import {
  ListSingleSelectionDialogComponent, ListSingleSelectionOption
} from '../dialogs/list-single-selection-dialog/list-single-selection-dialog.component';
import {
  CustomFeatDialogComponent,
  CustomFeatDialogResult
} from '../dialogs/custom-feat-dialog/custom-feat-dialog.component';
import {ShortRank} from '../models/characters/short-rank';
import {
  NewNpcTemplateDialogComponent,
  NewNpcTemplateDialogResult
} from '../dialogs/new-npc-template-dialog/new-npc-template-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {ChipsDialogComponent} from '../dialogs/chips-dialog/chips-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class DialogsService {

  constructor(private matDialog: MatDialog) {
  }

  public async getBooleanFromConfirmationDialog(title: string, text: string, cancelActionName?: string,
                                                confirmActionName?: string): Promise<boolean> {
    const dialogRef = this.matDialog.open(ConfirmationDialogComponent, {
      width: '400px',
      data: {
        title, text, cancelActionName, confirmActionName
      }
    });
    return await firstValueFrom<boolean>(dialogRef.afterClosed());
  }

  public async getStringFromInputDialog(title: string,
                                        text: string,
                                        label: string,
                                        defaultValue?: string,
                                        cancelActionName?: string,
                                        confirmActionName?: string,
                                        inputType?: string,
                                        isTextArea?: boolean,
                                        textAreaRows?: number,
                                        maxLength?: number,
                                        allowEmpty?: boolean): Promise<string> {
    const dialogRef = this.matDialog.open(TextInputDialogComponent, {
      width: '400px',
      data: {
        title, text, label, defaultValue, cancelActionName, confirmActionName, inputType, isTextArea, textAreaRows,
        maxLength, allowEmpty
      },
    });
    return await firstValueFrom<string>(dialogRef.afterClosed());
  }

  public async getNumberFromInputDialog(title: string,
                                        text: string,
                                        label: string,
                                        defaultValue?: string,
                                        cancelActionName?: string,
                                        confirmActionName?: string,
                                        allowEmpty?: boolean,
                                        maxValue?: number,
                                        minValue?: number
  ): Promise<number> {
    const dialogRef = this.matDialog.open(NumberInputDialogComponent, {
      width: '400px',
      data: {
        title, text, label, defaultValue, cancelActionName, confirmActionName, allowEmpty, maxValue, minValue
      }
    });
    return await firstValueFrom<number>(dialogRef.afterClosed());
  }

  public async getSingleOptionFromListDialog<T>(title: string,
                                                text: string,
                                                options: ListSingleSelectionOption[],
                                                defaultValue?: any,
                                                cancelActionName?: string,
                                                confirmActionName?: string,
                                                allowEmpty?: boolean,
                                                label?: string,
  ): Promise<T> {
    const dialogRef = this.matDialog.open(ListSingleSelectionDialogComponent, {
      width: '400px',
      data: {
        title, text, label, defaultValue, cancelActionName, confirmActionName, allowEmpty, options
      }
    });
    return await firstValueFrom<T>(dialogRef.afterClosed());
  }

  public async getChipsFromChipsDialog(title: string,
                                       text: string,
                                       defaultChips?: string[]
  ): Promise<string[]> {
    const dialogRef = this.matDialog.open(ChipsDialogComponent, {
      width: '400px',
      data: {
        title, text, defaultChips
      }
    });
    return await firstValueFrom<string[]>(dialogRef.afterClosed());
  }

  public async geNpcDataFromDialog(): Promise<{ name: string, dataVisibility: DataVisibility }> {
    const dialogRef = this.matDialog.open(NewNpcDialogComponent, {
      width: '400px',
      data: {}
    });
    return await firstValueFrom<{ name: string, dataVisibility: DataVisibility }>(dialogRef.afterClosed());
  }

  async getPoolDataFromDialog(pool: Pool, allowDelete: boolean): Promise<PoolDataDialogResult> {
    const dialogRef = this.matDialog.open(PoolDataDialogComponent, {
      width: '400px',
      data: {pool, allowDelete}
    });
    return await firstValueFrom<PoolDataDialogResult>(dialogRef.afterClosed());
  }

  async getNewCustomPoolDataFromDialog(): Promise<Pool> {
    const dialogRef = this.matDialog.open(PoolDataDialogComponent, {
      width: '400px',
      data: {pool: null, allowDelete: false}
    });
    const result = await firstValueFrom<PoolDataDialogResult>(dialogRef.afterClosed());
    return result ? result.pool : null;
  }

  async getNewStatusEffectDataFromDialog(name: string, statusEffectTemplate: StatusEffectTemplate):
    Promise<{ amount: number, text: string }> {
    const dialogRef = this.matDialog.open(StatusEffectDataDialogComponent, {
      width: '400px',
      data: {
        name, statusEffectTemplate
      }
    });
    return await firstValueFrom<{ amount: number, text: string }>(dialogRef.afterClosed());
  }

  async getXpSpend(): Promise<XpSpendDialogResult> {
    const dialogRef = this.matDialog.open(XpSpendDialogComponent, {
      width: '400px',
      data: {}
    });
    return await firstValueFrom<XpSpendDialogResult>(dialogRef.afterClosed());
  }

  async getXpGained(characters: ShortCharacter[]): Promise<XpGainedDialogResult> {
    const dialogRef = this.matDialog.open(XpGainedDialogComponent, {
      width: '800px',
      data: {sessionAmount: 4, characters, componentsNames: ['Blooper', 'Background Music']}
    });
    return await firstValueFrom<XpGainedDialogResult>(dialogRef.afterClosed());
  }

  async getStyleFromDialog(title: string,
                           text: string,
                           stylesOptions: string[],
                           cancelActionName?: string,
                           confirmActionName?: string): Promise<string> {
    const dialogRef = this.matDialog.open(StylesListSingleSelectionDialogComponent, {
      width: '400px',
      data: {title, text, stylesOptions, cancelActionName, confirmActionName}
    });
    return await firstValueFrom<string>(dialogRef.afterClosed());
  }

  async getCustomFeat(isUpgrade: boolean, currentData?: CustomFeatDialogResult): Promise<CustomFeatDialogResult> {
    const dialogRef = this.matDialog.open(CustomFeatDialogComponent, {
      width: '800px',
      data: {isUpgrade, currentData}
    });
    return await firstValueFrom<CustomFeatDialogResult>(dialogRef.afterClosed());
  }

  async getNewNpcTemplateFromDialog(ranks: ShortRank[]): Promise<NewNpcTemplateDialogResult> {
    const dialogRef = this.matDialog.open(NewNpcTemplateDialogComponent, {
      width: '800px',
      data: {ranks}
    });
    return await firstValueFrom<NewNpcTemplateDialogResult>(dialogRef.afterClosed());
  }
}
