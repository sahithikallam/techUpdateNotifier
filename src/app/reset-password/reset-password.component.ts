import { Component, OnInit, OnDestroy } from '@angular/core';
// import { OtpService } from '../Services/otp.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ResetPasswordService } from './reset-password.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent implements OnInit, OnDestroy {
  emailForm!: FormGroup;
  passwordForm!: FormGroup;
  otpForm!: FormGroup;
  errorMessage: string | null = null;
  showModal = false;
  isOtpSent = false;
  isPasswordReset = false;
  isLoading = false;
  forgetErrorMessage: string | null = null;

  countdown: number = 300;
  displayTime: string = '05:00';
  timer: any; // Hold timer reference

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private resetPassword: ResetPasswordService
  ) {}

  ngOnInit() {
    this.emailForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]]
    });
    this.otpForm = this.fb.group({
      otp: ['', [Validators.required, Validators.minLength(6), Validators.maxLength(6)]]
    });
    this.passwordForm = this.fb.group({
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  ngOnDestroy() {
    if (this.timer) {
      clearInterval(this.timer); // Clean up timer on component destruction
    }
  }

  closeForgotPasswordModal() {
    this.showModal = false;
    this.isOtpSent = false;
    this.isPasswordReset = false;
    this.emailForm.reset();
    this.otpForm.reset();
    this.passwordForm.reset();
    this.errorMessage = null;
  }

  onEmailSubmit() {
    this.isLoading = true;  // Start loading state
    this.resetPassword.sendOtp(this.emailForm.value).subscribe(
      data => {
        this.isOtpSent = true;
        this.errorMessage = '';
        this.startTimer();
        this.showModal = true;
        this.isLoading = false; // Stop loading state
      },
      error => {
        this.isLoading = false; // Stop loading state
        if (error.status === 404) {
          this.errorMessage = error.error.message;
        } else if (error.status === 400) {
          this.errorMessage = error.error.message;
        } else {
          this.errorMessage = 'An unexpected error occurred. Please try again.';
        }
      }
    );
  }

  startTimer(): void {
    this.timer = setInterval(() => {
      if (this.countdown > 0) {
        this.countdown--;
        const minutes = Math.floor(this.countdown / 60).toString().padStart(2, '0');
        const seconds = (this.countdown % 60).toString().padStart(2, '0');
        this.displayTime = `${minutes}:${seconds}`;
      } else {
        clearInterval(this.timer);
      }
    }, 1000);
  }

  onOtpSubmit() {
    if (this.otpForm.invalid) {
      this.otpForm.markAllAsTouched();
      this.errorMessage = 'Please enter a valid 6-digit OTP';
      return;
    }
    const payload = { ...this.emailForm.value, ...this.otpForm.value };
    this.resetPassword.verifyOtp(payload).subscribe(
      data => {
        this.isOtpSent = false;
        this.isPasswordReset = true;
        this.errorMessage = '';
      },
      error => {
        if (error.status === 400) {
          this.errorMessage = error.error.message;
        } else {
          this.errorMessage = 'An unexpected error occurred. Please try again.';
        }
      }
    );
  }

  onPasswordSubmit() {
    if (this.passwordForm.value.newPassword !== this.passwordForm.value.confirmPassword) {
      this.errorMessage = 'Password mismatch';
      return;
    }
    const payload = { ...this.emailForm.value, new_password: this.passwordForm.value.newPassword };
    this.resetPassword.resetPassword(payload).subscribe(
      (response: { message: any }) => {
        this.startTimer();
        alert(response.message);
        this.closeForgotPasswordModal();
        this.router.navigate(['/login']);
      },
      (error: { status: number; error: { message: string | null } }) => {
        if (error.status === 400) {
          this.errorMessage = error.error.message;
        } else {
          this.errorMessage = 'Failed to reset password. Please try again.';
        }
      }
    );
  }
}
