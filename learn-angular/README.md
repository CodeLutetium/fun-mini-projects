# LearnAngular

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 18.2.1. To generate new project: run `ng new <project name>`. [Notes](#angular-notes) by me below.

## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The application will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory.

## Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via a platform of your choice. To use this command, you need to first add a package that implements end-to-end testing capabilities.

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.

# Angular notes

## Components

Every component has the following core properties:

- A `@Componentdecorator` that contains some configuration
- An HTML template that controls what renders into the DOM
- A CSS selector that defines how the component is used in HTML
- A TypeScript class with behaviors such as managing state, handling user input, or fetching data from a server.

To generate a component, run `ng generate <schematic>` or `ng g <schematic>`.

To use a component, you need to:

- Import the component into the file
- Add it to the component's `imports` array
- Use the component's selector in the `template`

## Managing Dynamic Data

### What is state

State: properties that a component needs to track

### Defining a state

Define state with [class fields syntax](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Public_class_fields).

```typescript
// todo-list-item.component.ts
@Component({ ... })
export class TodoListItem {
  taskTitle = '';
  isComplete = false;
}
```

### Updating states

Define methods that can access class fields with `this` keyword.

```ts
// todo-list-item.component.ts
@Component({ ... })
export class TodoListItem {
  taskTitle = '';
  isComplete = false;
  completeTask() {
    this.isComplete = true;
  }
  updateTitle(newTitle: string) {
    this.taskTitle = newTitle;
  }
}
```

## Rendering Dynamic Templates

Use double curly brace `{{ }}` to indicate dynamic content.

```ts
@Component({
  selector: "todo-list-item",
  template: ` <p>Title: {{ taskTitle }}</p> `,
})
export class TodoListItem {
  taskTitle = "Read cup of coffee";
}
```

## Dynamic Properties

Wrap the desired property in square brackets to tell Angular that the assigned value is dynamic (i.e., not a static string).

```ts
@Component({
  selector: "sign-up-form",
  template: ` <button type="submit" [disabled]="formIsInvalid">Submit</button> `,
})
export class SignUpForm {
  formIsInvalid = true;
}
```

## Dynamic Attributes

Dynamically binding **custom** HTML attributes(eg. `aria-`, `data-`, etc).

**will NOT work:**

```ts
@Component({
  standalone: true,
  template: ` <button [data-test-id]="testId">Primary CTA</button> `,
})
export class AppBanner {
  testId = "main-cta";
}
```

Unfortunately, this will not work because custom HTML attributes are not standard DOM properties. In order for this to work as intended, we need to prepend the custom HTML attribute `with` the attr. prefix.

```ts
@Component({
  standalone: true,
  template: ` <button [attr.data-test-id]="testId">Primary CTA</button> `,
})
export class AppBanner {
  testId = "main-cta";
}
```

## Conditionals and Loops

Conditionally show and/or repeat content based on dynamic data.

### Conditional Rendering

#### `@if` block

```ts
// user-controls.component.ts
@Component({
  standalone: true,
  selector: "user-controls",
  template: `
    @if (isAdmin) {
    <button>Erase database</button>
    }
  `,
})
export class UserControls {
  isAdmin = true;
}
```

#### `@else` block

```ts
// user-controls.component.ts
@Component({
  standalone: true,
  selector: "user-controls",
  template: `
    @if (isAdmin) {
    <button>Erase database</button>
    } @else {
    <p>You are not authorized.</p>
    }
  `,
})
export class UserControls {
  isAdmin = true;
}
```

#### `@for` block

Used for rendering lists. Use `track` keyword.

```html
<!-- ingredient-list.component.html -->
<ul>
  @for (ingredient of ingredientList; track ingredient.name) {
  <li>{{ ingredient.quantity }} - {{ ingredient.name }}</li>
  }
</ul>
```

```ts
// ingredient-list.component.ts
@Component({
  standalone: true,
  selector: "ingredient-list",
  templateUrl: "./ingredient-list.component.html",
})
export class IngredientList {
  ingredientList = [
    { name: "noodles", quantity: 1 },
    { name: "miso broth", quantity: 1 },
    { name: "egg", quantity: 2 },
  ];
}
```

#### `track` property

When Angular renders a list of elements with `@for`, those items can later change or move. Angular needs to track each element through any reordering, usually by treating a property of the item as a unique identifier or key.

This ensures any updates to the list are reflected correctly in the UI and tracked properly within Angular, especially in the case of stateful elements or animations.

To accomplish this, we can provide a unique key to Angular with the `track` keyword.

## Handling User Interaction

### Event Handling

You can add an event handler to an element by:

1. Adding an attribute with the events name inside of parentheses
2. Specify what JavaScript statement you want to run when it fires

```ts
<button (click)="save()">Save</button>
```

For example, if we wanted to create a button that would run a `transformText` function when the `click` event is fired, it would look like the following:

```ts
// text-transformer.component.ts
@Component({
  standalone: true,
  selector: "text-transformer",
  template: `
    <p>{{ announcement }}</p>
    <button (click)="transformText()">Abracadabra!</button>
  `,
})
export class TextTransformer {
  announcement = "Hello again Angular!";
  transformText() {
    this.announcement = this.announcement.toUpperCase();
  }
}
```

If you need to access the event object, Angular provides an implicit `$event` variable that you can pass to a function:

```ts
<button (click)="createUser($event)">Submit</button>
```

## Dependency Injection

When you need to share logic between components, Angular leverages the design pattern of dependency injection that allows you to create a “service” which allows you to inject code into components while managing it from a single source of truth.

### Services

Services are reusable pieces of code that can be injected.

Comprises of the following:

- A TypeScript decorator that declares the class as an Angular service via `@Injectable` and allows you to define what part of the application can access the service via the `providedIn` property (which is typically `'root'`) to allow a service to be accessed anywhere within the application.
- A TypeScript class that defines the desired code that will be accessible when the service is injected

eg:
```ts
// Calculator service
import {Injectable} from '@angular/core';
@Injectable({
  providedIn: 'root',
})
export class CalculatorService {
  add(x: number, y: number) {
    return x + y;
  }
}
```

```ts
// Receipt component
import { Component, inject } from '@angular/core';
import { CalculatorService } from './calculator.service';
@Component({
  selector: 'app-receipt',
  template: `<h1>The total is {{ totalCost }}</h1>`,
})
export class Receipt {
  private calculatorService = inject(CalculatorService);
  totalCost = this.calculatorService.add(50, 25);
}
```