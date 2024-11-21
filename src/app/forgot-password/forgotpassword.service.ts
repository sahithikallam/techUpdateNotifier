// import { Injectable } from '@angular/core';
// import { HttpClient, HttpHeaders } from '@angular/common/http';
// import { Observable } from 'rxjs';

// @Injectable({
//   providedIn: 'root',
// })
// export class ForgotPasswordService {
//   private apiUrl = 'http://localhost:5000/user/reset-password'; // Adjust this URL as necessary

//   constructor(private http: HttpClient) {}

//   resetPassword(email: string): Observable<any> {
//     const headers = new HttpHeaders({
//       'Content-Type': 'application/json',
//     });

//     const body = {
//       email: email,
//     };

//     return this.http.post<any>(this.apiUrl, body, { headers: headers });
//   }
// }
