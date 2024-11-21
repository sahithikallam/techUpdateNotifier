import { Component } from '@angular/core';
import { UserService } from '../Services/user-service.service';

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent {
  user: any; 
  

  constructor(
    
    private userService: UserService
  ) {}

  ngOnInit(): void {
  
    this.getUserDetails();
   
  }
  getUserDetails(): void {
    this.userService.getUser().subscribe(data => {
      this.user = data;
      console.log(data);
    });
  }

}
