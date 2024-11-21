import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreviousUpdatesComponent } from './previous-updates.component';

describe('PreviousUpdatesComponent', () => {
  let component: PreviousUpdatesComponent;
  let fixture: ComponentFixture<PreviousUpdatesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PreviousUpdatesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PreviousUpdatesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
