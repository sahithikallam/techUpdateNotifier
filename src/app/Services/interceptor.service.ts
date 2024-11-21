import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor() {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Get the token from local storage or your preferred storage
    const token = localStorage.getItem('token');

    if (token) {
      // Clone the request and set the new header
      const cloned_request = request.clone({
        headers:request.headers.set('Authorization', 'Bearer '+token)
      });
      console.log(cloned_request)
      // console.log(token)
      return next.handle(cloned_request)
    }

    // Pass the cloned request instead of the original request to the next handle
    return next.handle(request);
  }
}
