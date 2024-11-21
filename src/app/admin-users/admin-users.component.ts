import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-users',
  templateUrl: './admin-users.component.html',
  styleUrls: ['./admin-users.component.css']
})
export class AdminUsersComponent implements OnInit {

  showUsers: boolean = false;
  users: any[] = [];
  user: any; // Store selected user
  isModalOpen: boolean = false; // Controls modal visibility
  private apiUrl = 'http://127.0.0.1:5000/admin'; // Your API URL

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.fetchUsers();
  }

  fetchUsers() {
    this.http.get<any[]>(`${this.apiUrl}/details`).subscribe(
      response => {
        console.log(response);
        this.users = response;
        this.showUsers = true;
      },
      error => {
        console.error('Error fetching users:', error);
      }
    );
  }

  openDeleteModal(user: any) {
    this.user = user;
    this.isModalOpen = true; // Show the modal
  }

  closeModal() {
    this.isModalOpen = false; // Close the modal
  }

  // deleteUser(userId: string) {
  //   this.http.delete(`${this.apiUrl}/user/delete/${userId}`).subscribe(
  //     response => {
  //       console.log(response);
  //       alert('User removed successfully!'); // Show alert after deletion
  //       this.fetchUsers();
  //       // Refresh the user list after deletion
  //       this.closeModal(); 
  //       // Close the modal
  //     },
  //     error => {
  //       console.error('Error deleting user:', error);
  //     }
  //   );
  // }
  deleteUser() {
    const userId = this.user.user_id
    this.http.delete(`${this.apiUrl}/user/delete/${userId}`).subscribe(
      response => {
        console.log(response);
        alert('User removed successfully!'); // Show alert after deletion
        this.fetchUsers(); // Refresh the user list after deletion
        this.closeModal(); // Close the modal
      },
      error => {
        console.error('Error deleting user:', error);
        alert('There was an error deleting the user. Please try again.');
        this.closeModal(); // Close the modal
      }
    );
  }
  
}
