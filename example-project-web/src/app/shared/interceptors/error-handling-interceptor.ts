import {catchError} from 'rxjs/operators';
import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import {Observable} from 'rxjs';
import {Injectable} from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';

@Injectable()
export class ErrorHandlingInterceptor implements HttpInterceptor {


  constructor(private _snackBar: MatSnackBar) {

  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        console.error(error);
        this._snackBar.open(error.error.detail || error.message , 'Ok', {duration: 10000});
        throw error;
      })
    );
  }
}
