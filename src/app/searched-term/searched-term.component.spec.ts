import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchedTermComponent } from './searched-term.component';

describe('SearchedTermComponent', () => {
  let component: SearchedTermComponent;
  let fixture: ComponentFixture<SearchedTermComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchedTermComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchedTermComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
