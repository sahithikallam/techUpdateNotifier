import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from '../subscriptions.service'; 
import { UserService } from '../Services/user-service.service'; 
import { TechnologyService } from '../technology.service';

@Component({
  selector: 'app-technologies',
  templateUrl: './technologies.component.html',
  styleUrls: ['./technologies.component.css']
})
export class TechnologiesComponent implements OnInit {
  technologies: any[] = [];
  userId: string = '';
  subscribedTechIds: Set<string> = new Set(); 
  selectedTech: any = null; 
  isModalOpen: boolean = false;


  constructor(
    private subscriptionService: SubscriptionService,
    private userService: UserService,
    private technologyService: TechnologyService
  ) {}

  ngOnInit(): void {
    this.loadUser();
    this.loadTechnologies();
  }

  loadUser() {
    this.userService.getUser().subscribe(user => {
      this.userId = user.user_id;
    });
  }

  loadTechnologies() {
    this.technologyService.getTechnologies().subscribe(data => {
      this.technologies = data;
      this.checkExistingSubscriptions();
    });
  }

  setSelectedTech(tech: any) {
    this.selectedTech = tech;
  }

  checkExistingSubscriptions() {
    this.subscriptionService.getSubscriptions(this.userId).subscribe(subscriptions => {
      subscriptions.forEach(sub => {
        this.subscribedTechIds.add(sub.tech_id);
      });
    });
  }

  subscribe(techId: string) {
    this.subscriptionService.subscribeToTechnology(this.userId, techId).subscribe(response => {
      alert('Subscribed successfully!');
      this.subscribedTechIds.add(techId); 
    });
  }

  isSubscribed(techId: string): boolean {
    return this.subscribedTechIds.has(techId); 
  }

  openInfoModal(tech: any) {
    this.selectedTech = tech;
    console.log('Selected Technology:', this.selectedTech); 
    this.isModalOpen = true; 
  }

  closeInfoModal() {
    this.selectedTech = null;
    this.isModalOpen = false; 
  }
}
