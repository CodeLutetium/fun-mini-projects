import { Routes } from '@angular/router';
import { AppComponent } from './app.component';
import { TableComponent } from './table/table.component';

export const routes: Routes = [
  { path: '', component: AppComponent },
  { path: 'table', component: TableComponent },
  { path: 'table/*', redirectTo: '/table' },
];
