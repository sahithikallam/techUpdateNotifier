// import { Component } from '@angular/core';
// import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// import { ForgotPasswordService } from './forgotpassword.service'; 

// @Component({
//   selector: 'app-forgot-password',
//   templateUrl: './forgot-password.component.html',
//   styleUrls: ['./forgot-password.component.css'],

// })
// export class ForgotPasswordComponent {
//   resetForm: FormGroup;
//   message: string | null = null;
//   router: any;

//   constructor(
//     private fb: FormBuilder,
//     private forgotPasswordService: ForgotPasswordService
//   ) {
//     this.resetForm = this.fb.group({
//       email: ['', [Validators.required, Validators.email]],
//     });
//   }

//   onSubmit(): void {
//     if (this.resetForm.valid) {
//       const email = this.resetForm.value.email;

//       this.forgotPasswordService.resetPassword(email).subscribe(
//         (response) => {
//           this.message = response.message;
//           this.resetForm.reset();
//         },
//         (error) => {
//           this.message = error.error.message || 'An error occurred';
//         }
//       );
//     }
//   }

// }
