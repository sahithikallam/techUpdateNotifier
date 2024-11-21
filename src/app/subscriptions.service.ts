import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  private apiUrl = 'http://127.0.0.1:5000/subscription';

  constructor(private http: HttpClient) {}

  getSubscriptions(userId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/subscriptions`, { params: { user_id: userId } })
      .pipe(
        catchError(err => {
          console.error('Error fetching subscriptions:', err);
          return throwError(err);
        })
      );
  }
  
  subscribeToTechnology(userId: string, techId: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/subscribe`, { user_id: userId, tech_id: techId })
      .pipe(
        catchError(err => {
          console.error('Error subscribing:', err);
          return throwError(err);
        })
      );
  }

  getAvailableTechnologies(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/technologies`)
      .pipe(
        catchError(err => {
          console.error('Error fetching available technologies:', err);
          return throwError(err);
        })
      );
  }

  unsubscribeFromTechnology(userId: string, techId: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/unsubscribe`, {
      user_id: userId,
      tech_id: techId
    }).pipe(
      catchError(err => {
        console.error('Error unsubscribing:', err);
        return throwError(err);
      })
    );
  }

  getPreviousUpdates(techId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/previous-updates/${techId}`)
      .pipe(
        catchError(err => {
          console.error('Error fetching previous updates:', err);
          return throwError(err);
        })
      );
  }
  
}
