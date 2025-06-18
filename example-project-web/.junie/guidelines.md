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

## Best Practices

1. Always add any RxJS subscriptions to the `subscriptions` array to prevent memory leaks
2. Set the breadcrumbs in the constructor using the appropriate method from `BreadcrumbsService`
3. Keep the component's path in `app.routes.ts` consistent with the URL methods in `RoutingService`
4. Follow the naming conventions used in the existing code
