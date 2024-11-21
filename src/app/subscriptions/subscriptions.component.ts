import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from '../subscriptions.service'; 
import { UserService } from '../Services/user-service.service'; 
import { Router } from '@angular/router'; // Import Router

interface Technology {
  tech_id: string;
  tech_name: string;
  tech_desc: string;
  version: string;
  tech_pic: string;
}

@Component({
  selector: 'app-subscription',
  templateUrl: './subscriptions.component.html',
  styleUrls: ['./subscriptions.component.css']
})
export class SubscriptionComponent implements OnInit {
  subscriptions: Technology[] = [];
  userId: string = '';
  availableTechnologies: Technology[] = [];
  filteredTechnologies: Technology[] = [];
  isLoading: boolean = true;
  selectedTech: any;  // variable to hold selected technology for unsubscribing


  constructor(
    private subscriptionService: SubscriptionService, 
    private userService: UserService,
    private router: Router // Inject Router
  ) {}

  ngOnInit(): void {
    this.loadUser();
    this.loadAvailableTechnologies();
  }

  setSelectedTech(tech: any) {
    this.selectedTech = tech;
  }

  loadUser() {
    this.userService.getUser().subscribe(user => {
      this.userId = user.user_id; 
      if (this.userId) {
        this.loadSubscriptions();
      } else {
        this.isLoading = false;
      }
    }, error => {
      this.isLoading = false;
    });
  }

  loadSubscriptions() {
    if (!this.userId) return;
  
    this.subscriptionService.getSubscriptions(this.userId).subscribe(data => {
      this.subscriptions = data; 
      this.isLoading = false;
      this.filterAvailableTechnologies();
    }, error => {
      this.isLoading = false;
    });
  }
  
  loadAvailableTechnologies() {
    this.subscriptionService.getAvailableTechnologies().subscribe(
      data => {
        this.availableTechnologies = data;
        this.filterAvailableTechnologies();
      },
      error => {
        console.error('Error fetching available technologies:', error);
      }
    );
  }

  filterAvailableTechnologies() {
    const subscribedTechIds = new Set(this.subscriptions.map(sub => sub.tech_id));
    this.filteredTechnologies = this.availableTechnologies.filter(tech => !subscribedTechIds.has(tech.tech_id));
  }

  subscribeToTechnology(techId: string) {
    this.subscriptionService.subscribeToTechnology(this.userId, techId).subscribe(
      () => {
        this.loadSubscriptions();
      },
      error => {
        console.error('Error subscribing:', error);
      }
    );
  }

  unsubscribe(techId: string) {
    this.subscriptionService.unsubscribeFromTechnology(this.userId, techId).subscribe(() => {
      this.loadSubscriptions();
    }, error => {
      console.error('Error unsubscribing:', error);
    });
  }


  viewUpdates(techId: string) {
    // Navigate to the PreviousUpdates component with the techId as a parameter
    this.router.navigate(['/previous-updates', { techId }]);
  }
}
