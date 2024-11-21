import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-navbar',
  templateUrl: './admin-navbar.component.html',
  styleUrls: ['./admin-navbar.component.css']
})
export class AdminNavbarComponent implements OnInit {
  showEditProfile: boolean = false; 
  adminData: any = {};   
  isEditing: boolean = false; // Track editing state

  private apiUrl = 'http://127.0.0.1:5000/admin'; 

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.fetchAdminData();
  }
 
  fetchAdminData() {
    const adminEmail = 'admin.sahithi@gmail.com'; 
    this.http.get<any>(`${this.apiUrl}/details?admin_email=${adminEmail}`).subscribe(
      (data: any) => {
        this.adminData = data; // Assign the admin data
        console.log('Admin data fetched:', this.adminData); // Log admin data for debugging
      },
      (error) => {
        console.error('Error fetching admin details:', error.message || error);
      }
    );
  }

  editProfile() {
    this.isEditing = true; // Set editing state to true
  }

  saveChanges() {
    this.http.put<any>(`${this.apiUrl}/update`, this.adminData).subscribe(
      (response) => {
        console.log('Profile updated successfully:', response);
        this.isEditing = false; // Stop editing
      },
      (error) => {
        console.error('Error saving changes:', error.message || error);
      }
    );
  }

  cancelEdit() {
    this.isEditing = false; // Stop editing
    this.fetchAdminData(); // Re-fetch data to revert any unsaved changes
  }
}

