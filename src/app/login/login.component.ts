import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { LoginService, LoginResponse } from '../Services/login-services.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  passwordType: string = 'password';
  message: string = '';
  toastr: any;


  constructor(private loginService: LoginService,  private router: Router) {}

  togglePassword() {
    this.passwordType = this.passwordType === 'password' ? 'text' : 'password';
  }

  onSubmit() {
    if (!this.email || !this.password) {
      this.message = 'Please fill all the fields.';
      return;
    }
  
    this.loginService.login(this.email, this.password).subscribe(
      (response: LoginResponse) => {
        console.log('Login successful:', response);
        this.loginService.setToken(response.token); 
        if (response.isAdmin !== undefined) {
          if (response.isAdmin) {
            this.router.navigate(['/admin']); 
          } else {
            this.router.navigate(['/user']); 
          }
          // alert(response.message+response.token); 
          // alert(response.message); 

          localStorage.setItem("token",response.token);
        //   this.router.navigate(['/user'], { replaceUrl: true });
        }
      },
      (error: any) => {
        console.error('Login error:', error);
        this.message = error?.error?.message || 'Invalid credentials. Please try again.';
      }
    );
  }
  
}
