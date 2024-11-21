import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ResetPasswordService {
  private api = 'http://127.0.0.1:5000/otp';  // Base URL for the API

  constructor(private http: HttpClient) { }

  resetPassword(payload: any): Observable<any> {
    return this.http.post(`${this.api}/reset-password`, payload);  // Should return Observable
  }

  sendOtp(payload: any): Observable<any> {
    return this.http.post(`${this.api}/forgot-password/send-otp`, payload);  // Use full API URL
  }

  verifyOtp(payload: any): Observable<any> {
    return this.http.post(`${this.api}/forgot-password/verify-otp`, payload);  // Use full API URL
  }
}
