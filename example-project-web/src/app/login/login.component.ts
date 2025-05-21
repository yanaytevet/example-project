import {Component, inject} from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import {loginView} from '../../generated-files/auth';
import {AuthenticationService} from '../shared/authentication/authentication.service';
import {Router} from '@angular/router';
import {RoutingService} from '../shared/services/routing.service';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  private authService = inject(AuthenticationService);
  private routingService = inject(RoutingService);
  private fb = inject(FormBuilder);
  loginForm: FormGroup = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required]
  });

  async tryLogin() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      await this.authService.tryLogin(username, password);
      if (this.authService.isLoggedIn()) {
        await this.routingService.navigateToHome();
      }
    }
  }
}
