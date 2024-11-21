import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TechnologyService {
  private apiUrl = 'http://127.0.0.1:5000/technology/technologies'; 
  private techId: string | null = null; // To store selected techId

  constructor(private http: HttpClient) {}

  getTechnologies(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  setTechId(techId: string): void {
    this.techId = techId;
  }

  getTechId(): string | null {
    return this.techId;
  }
}
