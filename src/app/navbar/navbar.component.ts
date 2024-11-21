import { Component, OnInit } from '@angular/core';
import { UserService } from '../Services/user-service.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isEditing: boolean = false;
  user: any = {}; // User object
  notifications: any[] = [];
  isChangingPassword: boolean = false;

  // Password fields
  currentPassword: string = '';
  newPassword: string = '';
  confirmNewPassword: string = '';

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.getUserDetails();
  }

  getUserDetails(): void {
    this.userService.getUser().subscribe(
      data => {
        this.user = data;
        console.log(data);
      },
      error => {
        console.error('Error fetching user data:', error);
      }
    );
  }

  // Edit profile mode
  editProfile() {
    this.isEditing = true;
  }

  // Save profile changes
  saveChanges(): void {
    if (!this.isChangingPassword) {
      this.isEditing = false;
      this.userService.updateUser(this.user).subscribe({
        next: () => alert('Profile updated successfully!'),
        error: () => alert('Error updating profile!')
      });
    } else {
      this.saveNewPassword();
    }
  }

  // Cancel editing mode
  cancelEdit(): void {
    this.isEditing = false;
    this.getUserDetails(); // Reset user data to original state
  }

  // Show password change form
  showChangePassword(): void {
    this.isChangingPassword = true;
    this.isEditing = false; // Switch off profile edit mode when changing password
  }

  // Save new password
  saveNewPassword(): void {
    if (this.newPassword !== this.confirmNewPassword) {
      alert('Passwords do not match!');
      return;
    }

    this.userService.changePassword({
      currentPassword: this.currentPassword,
      newPassword: this.newPassword
    }).subscribe({
      next: () => {
        alert('Password changed successfully!');
        this.cancelChangePassword(); // Close change password section
      },
      error: () => alert('Error changing password!')
    });
  }

  // Cancel password change
  cancelChangePassword(): void {
    this.isChangingPassword = false;
    this.currentPassword = '';
    this.newPassword = '';
    this.confirmNewPassword = '';
  }
}
