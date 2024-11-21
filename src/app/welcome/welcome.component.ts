import { Component, ElementRef, AfterViewInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.css']
})
export class WelcomeComponent implements AfterViewInit {
  private videoElement!: HTMLVideoElement;
  private playButtonElement!: HTMLElement;
  private pauseButtonElement!: HTMLElement;

  constructor(private el: ElementRef, private router: Router) {}

  ngAfterViewInit() {
    // Select the video and button elements
    this.videoElement = this.el.nativeElement.querySelector('#introVideo');
    this.playButtonElement = this.el.nativeElement.querySelector('#playButton');
    this.pauseButtonElement = this.el.nativeElement.querySelector('#pauseButton');

    // Check for null or undefined elements
    if (this.playButtonElement && this.pauseButtonElement) {
      // Initially, only show the play button
      this.playButtonElement.style.display = 'block';
      this.pauseButtonElement.style.display = 'none';
    }
  }

  // Method to toggle video play/pause
  toggleVideo(action: string) {
    if (this.videoElement) {
      if (action === 'play') {
        this.videoElement.play(); // Play the video
        this.playButtonElement.style.display = 'none'; // Hide play button
        this.pauseButtonElement.style.display = 'block'; // Show pause button
      } else if (action === 'pause') {
        this.videoElement.pause(); // Pause the video
        this.playButtonElement.style.display = 'block'; // Show play button
        this.pauseButtonElement.style.display = 'none'; // Hide pause button
      }
    }
  }

  redirectToLogin() {
    this.router.navigate(['/login']);
  }
}
