import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface User {
  user_id: string;
  email: string;
  // Add other fields as needed
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl: string = 'http://127.0.0.1:5000/user';
  private user: User | null = null; // Store user details with proper typing

  constructor(private http: HttpClient) {}

  // Get user data
  getUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}/getUser`);
  }

  // Signup method
  signup(data: { email: string; otp: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup`, data); 
  }

  // Send OTP for email verification
  sendOtp(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/sendOtp`, { email });
  }

  // Set the user details
  setUser(user: User): void {
    this.user = user;
  }

  // Get user ID (if the user is set)
  getUserId(): string | null {
    return this.user ? this.user.user_id : null; // Return null if user is not set
  }

  // Update user details
  updateUser(user: User): Observable<any> {
    return this.http.put(`${this.apiUrl}/editDetails`, user);
  }

  // Change user password
  changePassword(passwordData: { currentPassword: string; newPassword: string }): Observable<any> {
    console.log(passwordData);  // Log the password change payload
    return this.http.post(`${this.apiUrl}/user/changePassword`, passwordData);
  }
}
