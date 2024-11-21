import { Component, OnInit } from '@angular/core';
import { SubscriptionService } from '../subscriptions.service';
import { UserService } from '../Services/user-service.service';
import { Router } from '@angular/router';



interface Technology {
  tech_id: string;
  tech_name: string;
  tech_desc: string;
  version: string;
  tech_pic: string;
}

@Component({
  selector: 'app-earlier-updates',
  templateUrl: './earlier-updates.component.html',
  styleUrls: ['./earlier-updates.component.css']
})
export class EarlierUpdatesComponent implements OnInit {
  subscriptions: Technology[] = [];
  userId: string = '';
  filteredTechnologies: Technology[] = [];
  isLoading: boolean = true;


  constructor(
    private subscriptionService: SubscriptionService, 
    private userService: UserService,
    private router: Router // Inject Router
  ) {}

  ngOnInit(): void {
    this.loadUser();
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
      // console.log(data)
    }, error => {
      this.isLoading = false;
    });
  }
}
