import { Component, HostListener, OnInit } from '@angular/core';
import { TechnologyService } from '../technology.service';
import { SubscriptionService } from '../subscriptions.service';
import { UserService } from '../Services/user-service.service'; 
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  technologies: any[] = [];
  filteredTechnologies: { tech_name: string; tech_pic: string }[] = [];
  user: any; 
  userId: string = ''; 
  searchTerm: string = ''; 
  showTooltip: boolean = false; 
  techNews: { id: number; title: string }[] = [];
  todoTasks: string = ''; 
  showModal: boolean = false;
  selectedTech: any;

  constructor(
    private router: Router,  
    private technologyService: TechnologyService,
    private subscriptionService: SubscriptionService,
    private userService: UserService,
  ) {}

  ngOnInit(): void {
    this.loadTechnologies();
    this.getUserDetails();
    this.loadTechNews(); 
    this.loadTasks();
  }

  loadTechnologies() {
    this.technologyService.getTechnologies().subscribe(data => {
      this.technologies = data;
      this.filteredTechnologies = [...this.technologies];
    });
  }

  getUserDetails(): void {
    this.userService.getUser().subscribe(data => {
      this.user = data;
      this.userId = data?.user_id;
      if (this.userId) {
        this.loadTasks();
      }
    });
  }

  loadTechNews(): void {
    this.techNews = [
      { id: 1, title: 'Tech Update 1' },
      { id: 2, title: 'Tech Update 2' },
      { id: 3, title: 'Tech Update 3' },
    ];
  }

  subscribe(techId: string): void {
    const userId = this.userService.getUserId();
    if (!userId) {
      alert('User ID not found. Please log in again.');
      return;
    }

    this.subscriptionService.subscribeToTechnology(userId, techId).subscribe({
      next: (response: any) => {
        alert(response.message);
      },
      error: (err) => {
        alert('Error subscribing to technology: ' + err.message);
      }
    });
  }

  searchTechnology(): void {
    if (this.searchTerm.trim()) {
      console.log('Navigating to search:', this.searchTerm); // Debug log
      this.router.navigate(['/search', this.searchTerm]);
    } else {
      console.log('Search term is empty'); // Debug log
    }
  }
  

  filterTechnologies(): void {
    if (this.searchTerm) {
      const searchResult = this.technologies.filter(tech =>
        tech.tech_name.toLowerCase().includes(this.searchTerm.toLowerCase())
      );
      this.filteredTechnologies = [...searchResult];

      if (searchResult.length === 1) {
        this.openTechModal(searchResult[0]);
      }
    } else {
      this.filteredTechnologies = [...this.technologies];
    }
  }

  toggleTooltip(): void {
    this.showTooltip = !this.showTooltip;
  }

  closeTooltip(): void {
    this.showTooltip = false;
  }

  loadTasks(): void {
    if (this.userId) {
      const savedTasks = sessionStorage.getItem(`todoTasks_${this.userId}`);
      if (savedTasks) {
        this.todoTasks = savedTasks;
      }
    }
  }

  saveTasks(): void {
    if (this.userId) {
      sessionStorage.setItem(`todoTasks_${this.userId}`, this.todoTasks);
      alert('Tasks saved successfully!');
    } else {
      alert('User ID is not available. Please try logging in again.');
    }
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    if (!target.closest('.tooltip') && !target.closest('.icon')) {
      this.showTooltip = false;
    }
  }

  openTechModal(tech: any) {
    this.selectedTech = tech;
    this.showModal = true;
  }

  closeModal() {
    this.showModal = false;
    this.selectedTech = null;
  }

}
