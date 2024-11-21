import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private apiUrl = 'http://127.0.0.1:5000/user/user_notifications';

  constructor( private http: HttpClient) {}
 

  getNotifications(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  deleteNotification(notificationId: string): Observable<void> {
    // console.log(notificationId)
    return this.http.delete<void>(`${this.apiUrl}/${notificationId}`);
  }
 
 
}
