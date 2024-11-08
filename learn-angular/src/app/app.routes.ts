import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { TableComponent } from './table/table.component';
import { JavalinIntegrationExpComponent } from './javalin-integration-exp/javalin-integration-exp.component';

export const routes: Routes = [
  { path: '', component: AppComponent },
  { path: 'table', component: TableComponent },
  { path: 'test', component: JavalinIntegrationExpComponent },
  { path: 'table/*', redirectTo: '/table' },
];
