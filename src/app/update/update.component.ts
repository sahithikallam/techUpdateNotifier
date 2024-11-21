import { Component, OnInit } from '@angular/core';
import { UpdateService } from '../update.service';

@Component({
  selector: 'app-updates',
  templateUrl: './update.component.html',
  styleUrls: ['./update.component.css'] // Ensure this file exists as well
})
export class UpdateComponent implements OnInit {
  updates: any[] = [];
  newUpdate: any = { tech_id: '', update_type: '' };

  constructor(private updateService: UpdateService) {}

  ngOnInit(): void {
    this.loadUpdates();
  }

  loadUpdates(): void {
    this.updateService.getUpdates().subscribe(data => {
      this.updates = data;
    });
  }

  createUpdate(): void {
    this.updateService.createUpdate(this.newUpdate).subscribe(response => {
      alert(response.message);
      this.loadUpdates();
      this.newUpdate = { tech_id: '', update_type: '' };
    }, error => {
      alert('Error creating update');
    });
  }
}
