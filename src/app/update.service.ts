import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UpdateService {
  private apiUrl = 'http://127.0.0.1:5000/update'; // Your API endpoint

  constructor(private http: HttpClient) {}

  getUpdates(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  createUpdate(update: any): Observable<any> {
    return this.http.post(this.apiUrl, update);
  }
}
