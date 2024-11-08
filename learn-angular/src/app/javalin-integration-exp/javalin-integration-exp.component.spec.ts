import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JavalinIntegrationExpComponent } from './javalin-integration-exp.component';

describe('JavalinIntegrationExpComponent', () => {
  let component: JavalinIntegrationExpComponent;
  let fixture: ComponentFixture<JavalinIntegrationExpComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [JavalinIntegrationExpComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(JavalinIntegrationExpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
