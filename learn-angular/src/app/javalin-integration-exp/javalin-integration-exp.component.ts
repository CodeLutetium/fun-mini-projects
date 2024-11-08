import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

@Component({
  selector: 'app-javalin-integration-exp',
  standalone: true,
  imports: [],
  templateUrl: './javalin-integration-exp.component.html',
  styleUrl: './javalin-integration-exp.component.css'
})
export class JavalinIntegrationExpComponent {
  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<any[]>('http://localhost:7070/').subscribe(config => {
      // process the configuration.
      console.log(config);
      
    },
  err => {
    console.error('Error occurred:', err);
  });
  }
}
