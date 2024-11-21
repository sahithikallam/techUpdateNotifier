import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-admin-tech',
  templateUrl: './admin-tech.component.html',
  styleUrls: ['./admin-tech.component.css']
})
export class AdminTechComponent implements OnInit {
  showTechnologies: boolean = false;
  technologies: any;
  techName: string = ''; // Track technology name input
  techDescription: string = ''; // Track technology description input
  private apiUrl = 'http://127.0.0.1:5000/admin'; // Your API URL
  
  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.fetchTechnologies()
  }
  
  fetchTechnologies() {
    this.http.get<any>(`${this.apiUrl}/technologies`).subscribe(
      response => {
        console.log(response[0])
        this.technologies = response;
        this.showTechnologies = true;
      },
      error => {
        console.error('Error fetching technologies:', error);
      }
    );
  }

  deleteTechnology(techId: string) {
    if (confirm('Are you sure you want to delete this technology?')) {
      this.http.delete(`${this.apiUrl}/technology/delete/${techId}`).subscribe(
        response => {
          console.log('Technology deleted:', response);
          this.fetchTechnologies(); // Refresh the technology list after deletion
        },
        error => {
          console.error('Error deleting technology:', error);
        }
      );
    }
  }
}
