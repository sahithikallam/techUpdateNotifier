import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SubscriptionService } from '../subscriptions.service';


interface Technology {
  tech_id: string;
  tech_name: string;
  tech_desc: string;
  version: string;
  tech_pic: string;
}

@Component({
  selector: 'app-previous-updates',
  templateUrl: './previous-updates.component.html',
  styleUrls: ['./previous-updates.component.css']
})
export class PreviousUpdatesComponent implements OnInit {
  techId: string = ''; 
  updates: any[] = [];
  displayedUpdates: any[] = [];
  tech_name: string = '';
  itemsPerPage: number = 8; // Number of updates to display per page
  currentPage: number = 0; // Track the current page
  hasMoreUpdates: boolean = false; 
  showModal: boolean = false;
  selectedUpdate: any;
  isLoading: boolean = false;


  constructor(private route: ActivatedRoute, private subscriptionService: SubscriptionService) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.techId = params['techId']; // Retrieve techId
      if (this.techId) {
        this.fetchUpdates(); // Fetch updates for the technology
      } else {
        console.error('No techId provided');
      }
    });
  }

  fetchUpdates() {
    this.subscriptionService.getPreviousUpdates(this.techId).subscribe(
      (response: any) => {
        this.updates = response.updates; 
        this.hasMoreUpdates = this.updates.length > 0;
        this.loadMoreUpdates(); 
        // Load initial updates
        console.log('Updates:', this.updates);
      },
      (error) => {
        console.error('Error fetching updates:', error);
      }
    );
  }

  loadUpdates() {
    this.isLoading = true; // Start loading
    this.subscriptionService.getPreviousUpdates(this.techId).subscribe(
      (response) => {
        this.updates = response.updates; // Assuming response contains an 'updates' array
        this.isLoading = false; // Stop loading once data is fetched
        console.log('Updates:', this.updates);
      },
      (error) => {
        console.error('Error fetching updates:', error);
        this.isLoading = false; // Stop loading if there's an error
      }
    );
  }

  loadMoreUpdates() {
    const nextPageUpdates = this.updates.slice(this.currentPage * this.itemsPerPage, (this.currentPage + 1) * this.itemsPerPage);
    this.displayedUpdates.push(...nextPageUpdates);
    this.currentPage++;
    this.hasMoreUpdates = (this.currentPage * this.itemsPerPage) < this.updates.length; // Check if more updates exist
  }

  openModal(update: any) {
    this.selectedUpdate = update;
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.selectedUpdate = null;
  }
}
