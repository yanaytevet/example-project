import {AuthUser} from '../interfaces/users/auth-user';
import {PermissionsGuard} from './permissions-guard.service';
import {Injectable} from '@angular/core';

@Injectable()
export class AdminGuard extends PermissionsGuard {
  checkPermissions(authUser: AuthUser): boolean {
    return authUser?.user?.isAdmin;
  }
}
