import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EarlierUpdatesComponent } from './earlier-updates.component';

describe('EarlierUpdatesComponent', () => {
  let component: EarlierUpdatesComponent;
  let fixture: ComponentFixture<EarlierUpdatesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EarlierUpdatesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EarlierUpdatesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
