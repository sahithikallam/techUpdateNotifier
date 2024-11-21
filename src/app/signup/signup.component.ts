import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { OtpService } from '../Services/otp.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent {
  username: string = '';
  email: string = '';
  password: string = '';
  confirmPassword: string = '';
  acceptedTerms: boolean = false;
  otp: string = '';
  isOtpModalOpen: boolean = false;
  message: string = '';
  isSubmitting: boolean = false;
  isSuccess: boolean = false;

  passwordType: string = 'password';
  confirmPasswordType: string = 'password';

  constructor(private otpService: OtpService, private router: Router) {}

  onSubmit() {
    if (!this.formValid()) return;

    this.isSubmitting = true;
    this.otpService.sendOtp(this.email).subscribe(
      () => {
        this.isOtpModalOpen = true;
        this.message = 'OTP sent to your email.';
        this.isSubmitting = false;
      },
      (error) => {
        this.message = error.error?.message || 'Failed to send OTP.';
        this.isSubmitting = false;
      }
    );
  }

  verifyOtp() {
    this.isSubmitting = true;

    const payload = {
      email: this.email,
      otp: this.otp,
      user_name: this.username,
      password: this.password,
    };

    this.otpService.verifyOtp(payload).subscribe(
      () => {
        this.message = 'Signup successful! Redirecting to login...';
        this.isSuccess = true;
        setTimeout(() => this.router.navigate(['/login']));
      },
      (error) => {
        this.message = error.error?.message || 'Invalid OTP. Try again.';
        this.isSubmitting = false;
      }
    );
  }

  formValid(): boolean {
    return (
      !!this.username &&
      !!this.email &&
      !!this.password &&
      !!this.confirmPassword &&
      this.password === this.confirmPassword &&
      this.acceptedTerms === true
    );
  }

  togglePassword() {
    this.passwordType =
      this.passwordType === 'password' ? 'text' : 'password';
  }

  toggleConfirmPassword() {
    this.confirmPasswordType =
      this.confirmPasswordType === 'password' ? 'text' : 'password';
  }

  closeOtpModal() {
    this.isOtpModalOpen = false;
  }
}
