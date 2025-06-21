import {
  Injectable,
  Injector,
  InjectionToken,
  Type,
  inject,
} from '@angular/core';
import {
  Overlay,
  OverlayRef,
  OverlayConfig,
} from '@angular/cdk/overlay';
import { ComponentPortal } from '@angular/cdk/portal';
import { BaseDialogComponent } from './base-dialog.component';
import {
  ConfirmationDialogComponent,
  ConfirmationDialogInput
} from './common-dialogs/confirmation-dialog/confirmation-dialog.component';
import {
  NotificationDialogComponent,
  NotificationDialogInput
} from './common-dialogs/notification-dialog/notification-dialog.component';
import {
  NumberInputDialogComponent,
  NumberInputDialogInput
} from './common-dialogs/number-input-dialog/number-input-dialog.component';
import {
  TextInputDialogComponent,
  TextInputDialogInput
} from './common-dialogs/text-input-dialog/text-input-dialog.component';
import {
  SingleSelectionDialogComponent,
  SingleSelectionDialogInput
} from './common-dialogs/single-selection-dialog/single-selection-dialog.component';
import {
  MultipleSelectionDialogComponent,
  MultipleSelectionDialogInput
} from './common-dialogs/multiple-selection-dialog/multiple-selection-dialog.component';
import {DarkModeService} from '../services/dark-mode.service';

export const DIALOG_DATA = new InjectionToken<any>('DIALOG_DATA');

@Injectable({ providedIn: 'root' })
export class DialogService {
  private overlay = inject(Overlay);
  private injector = inject(Injector);
  private darkModeService = inject(DarkModeService);

  open<TInput, TOutput>(
      component: Type<BaseDialogComponent<TInput, TOutput>>,
      data?: TInput
  ): Promise<TOutput | null> {
    const overlayRef = this.overlay.create(this.getOverlayConfig());

    const injector = Injector.create({
      parent: this.injector,
      providers: [
        { provide: DIALOG_DATA, useValue: data },
        { provide: OverlayRef, useValue: overlayRef },
      ],
    });

    const portal = new ComponentPortal(component, null, injector);
    const componentRef = overlayRef.attach(portal);
    const instance = componentRef.instance;

    return new Promise<TOutput | null>((resolve) => {
      instance.closeDialog.subscribe((result: TOutput | null) => {
        resolve(result);
        overlayRef.dispose();
      });

      overlayRef.backdropClick().subscribe(() => {
        resolve(null);
        overlayRef.dispose();
      });

      overlayRef.keydownEvents().subscribe(event => {
        if (event.key === 'Escape') {
          resolve(null);
          overlayRef.dispose();
        }
      });
    });
  }

  private getOverlayConfig(): OverlayConfig {
    const isDarkMode = this.darkModeService.darkMode();
    return {
      hasBackdrop: true,
      backdropClass: isDarkMode ? 'cdk-overlay-black-backdrop' : 'cdk-overlay-dark-backdrop',
      positionStrategy: this.overlay
          .position()
          .global()
          .centerHorizontally()
          .centerVertically(),
    };
  }

  public async getBooleanFromConfirmationDialog(data: ConfirmationDialogInput): Promise<boolean> {
    const res = await this.open<ConfirmationDialogInput, boolean>(ConfirmationDialogComponent, data);
    return !!res;
  }

  public async showNotificationDialog(data: NotificationDialogInput): Promise<void> {
    await this.open<NotificationDialogInput, void>(NotificationDialogComponent, data);
  }

  public async getNumberFromInputDialog(data: NumberInputDialogInput): Promise<number | null> {
    return await this.open<NumberInputDialogInput, number | null>(NumberInputDialogComponent, data);
  }

  public async getTextFromInputDialog(data: TextInputDialogInput): Promise<string | null> {
    return await this.open<TextInputDialogInput, string | null>(TextInputDialogComponent, data);
  }

  public async getValueFromSelectionDialog(data: SingleSelectionDialogInput): Promise<any | null> {
    return await this.open<SingleSelectionDialogInput, any | null>(SingleSelectionDialogComponent, data);
  }

  public async getValuesFromMultipleSelectionDialog(data: MultipleSelectionDialogInput): Promise<any[] | null> {
    return await this.open<MultipleSelectionDialogInput, any[] | null>(MultipleSelectionDialogComponent, data);
  }
}
