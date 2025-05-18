import { Component } from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {AuthenticationService} from '../../shared/authentication/authentication.service';
import {AuthUser} from '../../shared/interfaces/users/auth-user';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-login-page',
  templateUrl: './login-page.component.html',
  styleUrls: ['./login-page.component.scss']
})
export class LoginPageComponent {
  failedLogin = false;
  failedLoginMsg = '';

  loginForm: FormGroup = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required])
  });

  constructor(private authService: AuthenticationService,
              private activeRoute: ActivatedRoute,
              private router: Router) {
  }

  async tryLogin() {
    const authUser: AuthUser = await this.authService.login(this.loginForm.value.username, this.loginForm.value.password);
    if (!authUser.is_authenticated) {
      this.failedLogin = true;
      this.failedLoginMsg = authUser.msg;
      return;
    }
    const nextUrl = this.activeRoute.snapshot.queryParams['redirectUrl'] || '/';
    await this.router.navigate([nextUrl]);
  }
}
