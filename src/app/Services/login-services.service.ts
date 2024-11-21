import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LoginResponse {
  message: string;
  isAdmin: boolean;
  token: string; // Add token to the response
}

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  private apiUrl: string = 'http://127.0.0.1:5000/user/login'; 

  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<LoginResponse> {
    const body = { email, password };
    
    return this.http.post<LoginResponse>(this.apiUrl, body, {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    });
  }

  // Method to store the JWT token
  setToken(token: string) {
    localStorage.setItem('token', token);
  }

  // Method to retrieve the JWT token
  getToken() {
    return localStorage.getItem('token');
  }

  isLoggedIn() {
    const token = this.getToken();
    return token != null; 
  }
}
