// src/app/Services/otp.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class OtpService {
  resetPassword(payload: any) {
    throw new Error('Method not implemented.');
  }
  private baseUrl = 'http://localhost:5000/otp'; // Update this URL as per your backend

  constructor(private http: HttpClient) {}

  sendOtp(email: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/send-otp`, { email });
  }

  // Change this method to accept an object
  verifyOtp(payload: { email: string; otp: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/verify-otp`, payload);
  }
}
