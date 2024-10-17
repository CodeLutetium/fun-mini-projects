import { Component } from '@angular/core';

// text-transformer.component.ts
@Component({
  standalone: true,
  selector: 'text-transformer',
  template: `
    <p>{{ announcement }}</p>
    <button (click)="transformText()">Abracadabra!</button>
  `,
})
export class TextTransformer {
  announcement = 'Hello again Angular!';
  transformText() {
    this.announcement = this.announcement.toUpperCase();
  }
}
