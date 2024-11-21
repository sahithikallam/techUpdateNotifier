import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminTechComponent } from './admin-tech.component';

describe('AdminTechComponent', () => {
  let component: AdminTechComponent;
  let fixture: ComponentFixture<AdminTechComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AdminTechComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AdminTechComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
