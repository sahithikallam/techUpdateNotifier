import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TechnologyService } from '../technology.service';
import { Location } from '@angular/common';

interface Technology {
  tech_name: string;
  tech_pic: string;
  version: string;
  info: string;
  tech_desc: string;
}

@Component({
  selector: 'app-searched-term',
  templateUrl: './searched-term.component.html',
  styleUrls: ['./searched-term.component.css']
})
export class SearchedTermComponent implements OnInit {
  searchTerm: string = '';
  matchingTechnologies: Technology[] = []; // Stores multiple matches
  statusMessage: string = '';
  isLoading: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private technologyService: TechnologyService,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.searchTerm = params['term'];
      this.searchTechnology();
    });
  }

  searchTechnology(): void {
    this.isLoading = true;
    this.technologyService.getTechnologies().subscribe({
      next: (technologies: Technology[]) => {
        // Filter technologies based on partial match
        this.matchingTechnologies = technologies.filter(tech =>
          tech.tech_name.toLowerCase().includes(this.searchTerm.toLowerCase())
        );

        // Set appropriate status message
        this.statusMessage = this.matchingTechnologies.length
          ? ''
          : `No technologies found containing "${this.searchTerm}".`;

        this.isLoading = false;
      },
      error: () => {
        this.statusMessage =
          'Error fetching technology details. Please try again later.';
        this.matchingTechnologies = [];
        this.isLoading = false;
      }
    });
  }

  goBack(): void {
    this.location.back(); // Navigate back to the previous page
  }
}
