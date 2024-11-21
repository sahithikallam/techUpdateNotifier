import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-sidebar',
  templateUrl: './admin-sidebar.component.html',
  styleUrls: ['./admin-sidebar.component.css']
})
export class AdminSidebarComponent implements OnInit {
  showUsers: boolean = false;
  showTechnologies: boolean = false;
  showNotifications: boolean = false;
  showEditProfile: boolean = false; // To control the visibility of the edit profile box
  users: any[] = [];
  technologies: any[] = [];
  notifications: any[] = [];
  techName: string = ''; // Track technology name input
  techDescription: string = ''; // Track technology description input
  adminData: any = {}; // Initialize adminData

  private apiUrl = 'http://127.0.0.1:5000/admin'; // Your API URL
  snackBar: any;
  showAddTechnology: any;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {}
  
  fetchUsers() {
    this.http.get<any[]>(`${this.apiUrl}/details`).subscribe(
      response => {
        this.users = response;
        this.showUsers = true;
        this.showTechnologies = false;
        this.showNotifications = false;
        this.showEditProfile = false; // Hide edit profile section
      },
      error => {
        console.error('Error fetching users:', error);
      }
    );
  }

  fetchTechnologies() {
    this.http.get<any[]>(`${this.apiUrl}/technologies`).subscribe(
      response => {
        this.technologies = response;
        this.showUsers = false;
        this.showTechnologies = true;
        this.showNotifications = false;
        this.showEditProfile = false; // Hide edit profile section
      },
      error => {
        console.error('Error fetching technologies:', error);
      }
    );
  }

  fetchNotifications() {
    this.http.get<any[]>(`${this.apiUrl}/notifications`).subscribe(
      response => {
        this.notifications = response;
        this.showUsers = false;
        this.showTechnologies = false;
        this.showNotifications = true;
        this.showEditProfile = false; // Hide edit profile section
      },
      error => {
        console.error('Error fetching notifications:', error);
      }
    );
  }

  // getTotalUsers() {
  //   this.http.get<any>(`${this.apiUrl}/total-users`).subscribe(
  //     response => {
  //       this.totalUsers = response.count;
  //     },
  //     error => {
  //       console.error('Error fetching total users:', error);
  //     }
  //   );
  // }

  // getTotalTechnologies() {
  //   this.http.get<any>(`${this.apiUrl}/total-technologies`).subscribe(
  //     response => {
  //       this.totalTechnologies = response.count;
  //     },
  //     error => {
  //       console.error('Error fetching total technologies:', error);
  //     }
  //   );
  // }

  deleteUser(userId: string) {
    if (confirm('Are you sure you want to delete this user?')) {
      this.http.delete(`${this.apiUrl}/user/delete/${userId}`).subscribe(
        response => {
          console.log(response);
          this.fetchUsers(); // Refresh the user list after deletion
        },
        error => {
          console.error('Error deleting user:', error);
        }
      );
    }
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

  logout() {
    this.router.navigate(['/login']); // Redirect to login page
  }


  toggleAddTechnology() {
    this.showAddTechnology = !this.showAddTechnology;
  }

  saveTechnology() {
    if (this.techName && this.techDescription) {
      this.http.post(`${this.apiUrl}/technologies`, { tech_name: this.techName, tech_desc: this.techDescription })
        .subscribe(response => {
          this.snackBar.open(`New technology ${this.techName} added!`, 'Close', { duration: 3000 });
          this.techName = ''; // Clear input
          this.techDescription = ''; // Clear input
          this.toggleAddTechnology(); // Hide the form after saving
          this.fetchTechnologies(); // Refresh technology list
        }, error => {
          console.error('Error adding technology:', error);
          this.snackBar.open('Failed to add technology.', 'Close', { duration: 3000 });
        });
    } else {
      this.snackBar.open('Please fill in all fields.', 'Close', { duration: 3000 });
    }
  }
}
