import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-add-technology',
  templateUrl: './add-technology.component.html',
  styleUrls: ['./add-technology.component.css']
})
export class AddTechnologyComponent {
  techName: string = '';
  techDescription: string = '';
  techReleases: string = ''; // New field
  techInfo: string = ''; // New field
  techPic: File | null = null; // File type for image
  version: string = ''; // Corrected field name
  private apiUrl = 'http://127.0.0.1:5000/admin/addTechnologies'; // Your API URL

  constructor(private http: HttpClient, private router: Router) {}

  // This method is triggered when the user selects a file
  onFileChange(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.techPic = file; // Store the selected file
    }
  }

  addTechnology() {
    if (!this.techName || !this.techDescription || !this.techPic) {
      alert('Please provide all the details and upload a picture!');
      return;
    }

    const formData = new FormData();
    formData.append('tech_name', this.techName);
    formData.append('tech_desc', this.techDescription);
    formData.append('releases', this.techReleases);
    formData.append('info', this.techInfo);
    formData.append('tech_pic', this.techPic, this.techPic.name); // Append the image file
    formData.append('version', this.version);

    this.http.post<{ tech_id: string; tech_name: string; tech_desc: string }>(this.apiUrl, formData).subscribe(
      (response) => {
        alert(`New technology ${response.tech_name} added successfully.`);
        this.techName = ''; // Clear the input fields
        this.techDescription = '';
        this.techReleases = ''; // Clear techReleases
        this.techInfo = ''; // Clear techInfo
        this.techPic = null; // Clear techPic
        this.version = ''; // Clear version

        this.router.navigate(['/admin']);
      },
      (error) => {
        console.error('Error adding technology:', error);
        alert('There was an error adding the technology.');
      }
    );
  }
}
