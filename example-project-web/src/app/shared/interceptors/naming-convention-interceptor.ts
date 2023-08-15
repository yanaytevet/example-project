import {catchError, map} from 'rxjs/operators';
import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse
} from '@angular/common/http';
import {Observable, throwError} from 'rxjs';
import {Injectable} from '@angular/core';
import * as humps from 'humps';

@Injectable()
export class NamingConventionInterceptor implements HttpInterceptor {


  constructor() {

  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const cloneReq = req.clone({
      body: humps.decamelizeKeys(req.body)
    });

    return next.handle(cloneReq).pipe(
      map((evt: HttpEvent<any>) => {
          if (evt instanceof HttpResponse) {
            const camelCaseObj = humps.camelizeKeys(evt.body);
            return evt.clone({body: camelCaseObj});
          }
          return evt;
        }
      ),
      catchError((error: HttpErrorResponse) => {
        throw error;
      })
    );
  }
}
