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

export const DIALOG_DATA = new InjectionToken<any>('DIALOG_DATA');

@Injectable({ providedIn: 'root' })
export class DialogService {
  private overlay = inject(Overlay);
  private injector = inject(Injector);

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
      instance.close.subscribe((result: TOutput | null) => {
        resolve(result);
        overlayRef.dispose();
      });

      overlayRef.backdropClick().subscribe(() => {
        resolve(null);
        overlayRef.dispose();
      });
    });
  }

  private getOverlayConfig(): OverlayConfig {
    return {
      hasBackdrop: true,
      backdropClass: 'cdk-overlay-dark-backdrop',
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
}
