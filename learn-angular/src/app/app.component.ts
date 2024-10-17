import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TodoListComponent } from './todo-list/todo-list.component';
import { TextTransformer } from './text-transformer/text-transformer.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, TodoListComponent, TextTransformer],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'learn-angular';
}
