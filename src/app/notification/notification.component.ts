import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router'; 
import { NotificationService } from '../notification.service';
@Component({
  selector: 'app-notification',
  templateUrl: './notification.component.html',
  styleUrls: ['./notification.component.css']
})
export class NotificationComponent implements OnInit {
  notifications: any[] = [];
  dismissedNotifications: any[] = [];
  filteredNotifications: any[] = [];

  constructor(private notificationService: NotificationService, private router: Router) {}

  ngOnInit(): void {
    this.getNotifications();
    

  }

  getNotifications(): void {
    this.notificationService.getNotifications().subscribe((data) => {
      console.log('Notifications from backend:', data);
      this.notifications = data;
      this.filteredNotifications = data; // Initially show all notifications
    });
  }

  // Dismiss a notification
  dismissNotification(id: string): void {
    const notificationIndex = this.notifications.findIndex(n => n.id === id);
    if (notificationIndex > -1) {
      const dismissedNotif = this.notifications.splice(notificationIndex, 1)[0];
      this.dismissedNotifications.push(dismissedNotif);
    }
    // Optionally: Mark it as dismissed in the backend (uncomment this part if needed)
    // this.notificationService.dismissNotification(id).subscribe();
  }

  // Filter notifications based on selection
  filterNotifications(event: any): void {
    const filterValue = event.target.value;
    if (filterValue === 'dismissed') {
      this.filteredNotifications = this.dismissedNotifications;
    } else {
      this.filteredNotifications = this.notifications;
    }
  }

  deleteNotification(id: string): void {
    this.notificationService.deleteNotification(id).subscribe(() => {
      this.notifications = this.notifications.filter(n => n.id !== id);
      this.dismissedNotifications = this.dismissedNotifications.filter(n => n.id !== id);
    });
  }

}
  //   goBack() {
  //   window.history.back(); 
  // }



//   ngOnInit(): void {
//     this.fetchNotifications();
//   }

//   fetchNotifications(): void {
//     this.notificationService.getNotifications().subscribe(
//       (data: any[]) => {
//         this.notifications = data;
//         console.log(data)
//       },
//       (error: any) => {
//         console.error('Error fetching notifications', error);
//       }
//     );
//   }

//   viewUpdate(notification: any): void {
//     this.router.navigate(['/update', notification.noti_id]); 
    
//   }

//   deleteNotification(notificationId: string): void {
//     console.log(notificationId)
//     this.notificationService.deleteNotification(notificationId).subscribe(
//       () => {
//         this.notifications = this.notifications.filter(n => n.id !== notificationId);
//       },
//       (error: any) => {
//         console.error('Error deleting notification', error);
//       }
//     );
//   }

//   goBack() {
//     window.history.back(); 
//   }

// }
