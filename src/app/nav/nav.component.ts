import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-nav',
  templateUrl: './nav.component.html',
  styleUrls: ['./nav.component.css']
})
export class NavComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  // Method to handle navigation to "About Us" section or route
  redirectToAbout(): void {
    this.router.navigate(['/about']); // Navigate to the "About" page
  }

  // Method to handle navigation to "Contact Us" section or route
  redirectToContact(): void {
    this.router.navigate(['/contact']); // Navigate to the "Contact" page
  }

  // Method to handle navigation to "Login" page
  redirectToLogin(): void {
    this.router.navigate(['/login']); // Navigate to the "Login" page
  }

  // Method to handle navigation to "Sign Up" page
  redirectToSignUp(): void {
    this.router.navigate(['/signup']); // Navigate to the "Sign Up" page
  }
}
