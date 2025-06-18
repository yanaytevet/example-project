# Guidelines for Adding a Page Component

When adding a new page component to the project, follow these guidelines to ensure consistency and proper integration with the application's architecture.

## 1. Create the Component

Create a new component that extends `BasePageComponent`:

```typescript
import { Component, inject } from '@angular/core';
import { BasePageComponent } from '../shared/components/base-page-component';
import { BreadcrumbsService } from '../shared/components/breadcrumbs/breadcrumbs.service';

@Component({
  selector: 'app-your-component',
  imports: [
    // Add necessary imports here
    BreadcrumbsComponent,
    // Other components, directives, pipes
  ],
  templateUrl: './your-component.component.html',
  styleUrl: './your-component.component.css'
})
export class YourComponent extends BasePageComponent {
  breadcrumbsService = inject(BreadcrumbsService);

  constructor() {
    super();
    // Set breadcrumbs
    this.breadcrumbs = this.breadcrumbsService.getYourComponentBreadcrumbs();

    // Add any subscriptions to this.subscriptions array
    // Example:
    // this.subscriptions.push(
    //   someObservable.subscribe(() => {
    //     // Handle the subscription
    //   })
    // );
  }
}
```

## 2. Add Route to app.routes.ts

Add your component to the application routes in `app.routes.ts`:

```typescript
// Inside the children array of the main route
{
    path: 'your-component-path',
    loadComponent: () =>
        import('./your-component/your-component.component').then(m => m.YourComponent),
    canActivate: [loggedInGuard] // Add guards as needed
}
```

## 3. Add Methods to RoutingService

Add navigation methods for your component in `RoutingService`:

```typescript
// Your Component route
getYourComponentUrl(): UrlTree {
  return this.router.createUrlTree(['/your-component-path']);
}

navigateToYourComponent(): Promise<boolean> {
  return this.router.navigateByUrl(this.getYourComponentUrl());
}
```

## 4. Add Breadcrumbs to BreadcrumbsService

Add a method to get breadcrumbs for your component in `BreadcrumbsService`:

```typescript
public getYourComponentBreadcrumbs(): LinkItem[] {
  return [
    {text: 'Home', linkArr: this.routingService.getHomeUrl(), active: true},
    {text: 'Your Component', linkArr: this.routingService.getYourComponentUrl(), active: true},
  ];
}
```

## Benefits of Extending BasePageComponent

By extending `BasePageComponent`, your component inherits:

1. Subscription management through the `subscriptions` array (from `BaseComponent`)
2. Automatic unsubscription when the component is destroyed (from `BaseComponent`)
3. Breadcrumbs functionality through the `breadcrumbs` property (from `BasePageComponent`)

## Angular 19+ Modern Syntax

This project uses Angular 19+ modern syntax features. Here are the key patterns to follow:

### 1. Signals, Input, and Output

Use the new signal-based input and output instead of decorators:

```typescript
import { Component, input, output } from '@angular/core';

@Component({
  selector: 'app-your-component',
  standalone: true,
  // ...
})
export class YourComponent {
  // Input signal (replaces @Input decorator)
  userName = input<string>('default value');

  // Optional input signal
  optionalData = input<SomeType | undefined>(undefined);

  // Required input signal
  requiredData = input.required<SomeType>();

  // Output signal (replaces @Output decorator)
  userClicked = output<void>();

  // Output with data
  dataChanged = output<SomeType>();

  // Usage example
  handleClick() {
    this.userClicked.emit();
    this.dataChanged.emit(someData);
  }
}
```

### 2. Control Flow with @if and @for

Use the new control flow syntax instead of structural directives:

```html
<!-- Use @if instead of *ngIf -->
@if (condition) {
  <div>Content to show when condition is true</div>
} @else {
  <div>Content to show when condition is false</div>
}

<!-- Use @for instead of *ngFor -->
@for (item of items; track item.id) {
  <div>{{ item.name }}</div>
} @empty {
  <div>No items available</div>
}
```

### 3. Dependency Injection with inject()

Use the `inject()` function instead of constructor injection:

```typescript
import { Component, inject } from '@angular/core';
import { SomeService } from './some.service';

@Component({
  // ...
})
export class YourComponent {
  // Inject services using the inject function
  private someService = inject(SomeService);
  private anotherService = inject(AnotherService);

  // Use injected services
  doSomething() {
    this.someService.method();
  }
}
```

## Best Practices

1. Always add any RxJS subscriptions to the `subscriptions` array to prevent memory leaks
2. Set the breadcrumbs in the constructor using the appropriate method from `BreadcrumbsService`
3. Keep the component's path in `app.routes.ts` consistent with the URL methods in `RoutingService`
4. Follow the naming conventions used in the existing code
5. Use modern Angular 19+ syntax (signals, @if/@for, inject) throughout the application

## CSS and Styling with Tailwind

This project uses Tailwind CSS for styling. Follow these guidelines for consistent styling:

### 1. Use Tailwind Instead of Component-Specific CSS

- We use Tailwind CSS for styling components
- No need to create CSS files per component
- Apply Tailwind utility classes directly in your HTML templates

```html
<!-- Example of using Tailwind classes -->
<div class="flex items-center justify-between p-4 bg-layer-1 rounded-lg">
  <h2 class="text-xl font-semibold">Title</h2>
  <button class="px-4 py-2 text-white bg-primary-500 rounded hover:bg-primary-600">
    Action
  </button>
</div>
```

### 2. Theme Colors

- Don't use colors directly in components as they might change with the theme
- Don't use Tailwind color classes like `gray-300` as they might change with the theme
- Use theme-specific classes instead:
  - Use `bg-layer-2` for background layers
  - Use `shadow-1` for shadow effects
  - Use theme colors for text, backgrounds, borders, and shadows

```html
<!-- ❌ Don't use direct color values or Tailwind color classes -->
<div class="text-[#FF0000] bg-[#EEEEEE]">Incorrect usage</div>
<div class="bg-gray-300 shadow-md">Incorrect usage</div>

<!-- ✅ Use theme-specific classes instead -->
<div class="text-primary-500 bg-layer-2 shadow-1">Correct usage</div>
```

### 3. Reusable Components

- Create general CSS classes for repeating components like:
  - Input fields
  - Buttons
  - Cards
  - Form elements

```css
/* In a shared styles file */
.btn-primary {
  @apply px-4 py-2 text-white bg-primary-500 rounded hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-primary;
}

.input-field {
  @apply w-full px-3 py-2 border border-layer-3 rounded focus:outline-none focus:ring-2 focus:ring-primary;
}
```

```html
<!-- Using the reusable classes -->
<button class="btn-primary">Submit</button>
<input type="text" class="input-field" placeholder="Enter your name">
```
