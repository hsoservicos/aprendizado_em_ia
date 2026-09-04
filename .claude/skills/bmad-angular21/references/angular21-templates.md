# Angular 21 — Templates de Código

## Template 1: Zoneless State com Signals
```typescript
import { Component, signal, computed, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-counter',
  standalone: true,
  template: `
    <button (click)="increment()">Count: {{ count() }}</button>
    <p>Double: {{ double() }}</p>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class CounterComponent {
  readonly count = signal(0);
  readonly double = computed(() => this.count() * 2);

  increment(): void {
    this.count.update(c => c + 1);
  }
}
```

## Template 2: Signal Forms
```typescript
import { Component, signal } from '@angular/core';
import { form, Field, required, email, minLength } from '@angular/forms/signals';

@Component({
  selector: 'app-account-settings',
  standalone: true,
  imports: [Field],
  template: `
    <form (submit)="saveAccount($event)">
      <div>
        <label>Email</label>
        <input [field]="accountForm.email" type="email" />
        @if (accountForm.email.errors()?.required) {
          <span class="error">Email is required</span>
        }
      </div>
      <div>
        <label>Username</label>
        <input [field]="accountForm.username" type="text" />
      </div>
      <button type="submit" [disabled]="!accountForm.valid()">Save</button>
    </form>
  `
})
export class AccountSettingsComponent {
  readonly formModel = signal({
    email: '',
    username: '',
    details: { bio: '' }
  });

  readonly accountForm = form(this.formModel, {
    validators: {
      email: [required(), email()],
      username: [required(), minLength(4)]
    }
  });

  saveAccount(event: Event): void {
    event.preventDefault();
    if (this.accountForm.valid()) {
      console.log('Saved:', this.accountForm.value());
    }
  }
}
```

## Template 3: Control Flow & @let
```html
<!-- @if / @else -->
@if (user()) {
  <h2>Welcome, {{ user()!.name }}</h2>
} @else {
  <p>Please log in</p>
}

<!-- @for com track e @empty -->
@for (item of items(); track item.id) {
  <li>{{ item.name }}</li>
} @empty {
  <li>No items found</li>
}

<!-- @switch -->
@switch (role()) {
  @case ('admin') {
    <app-admin-panel />
  }
  @case ('user') {
    <app-user-panel />
  }
  @default {
    <app-guest-panel />
  }
}

<!-- @let para variáveis -->
@let userName = user()?.name ?? 'Guest';
<p>Hello, {{ userName }}</p>
```

## Template 4: Angular ARIA — Menu
```typescript
import { Component } from '@angular/core';
import { MenuTrigger, Menu, MenuItem } from '@angular/aria';

@Component({
  selector: 'app-nav-menu',
  standalone: true,
  imports: [MenuTrigger, Menu, MenuItem],
  template: `
    <button [menuTrigger]="menuRef">Options</button>
    <ng-template #menuRef>
      <div role="menu">
        <div role="menuitem" (click)="edit()">Edit</div>
        <div role="menuitem" (click)="delete()">Delete</div>
        <div role="menuitem" (click)="share()">Share</div>
      </div>
    </ng-template>
  `
})
export class NavMenuComponent {
  edit(): void { /* ... */ }
  delete(): void { /* ... */ }
  share(): void { /* ... */ }
}
```

## Template 5: Vitest Test
```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/angular';
import { CounterComponent } from './counter.component';

describe('CounterComponent', () => {
  it('should display initial count', async () => {
    await render(CounterComponent);
    expect(screen.getByRole('button').textContent).toContain('Count: 0');
  });

  it('should increment on click', async () => {
    await render(CounterComponent);
    await fireEvent.click(screen.getByRole('button'));
    expect(screen.getByRole('button').textContent).toContain('Count: 1');
  });

  it('should handle async operations with fake timers', async () => {
    vi.useFakeTimers();
    const spy = vi.fn();
    setTimeout(spy, 1000);
    vi.advanceTimersByTime(1000);
    expect(spy).toHaveBeenCalledOnce();
    vi.useRealTimers();
  });
});
```

## Template 6: Resource API (Async Data)
```typescript
import { Component, resource, signal } from '@angular/core';

@Component({
  selector: 'app-user-profile',
  standalone: true,
  template: `
    @if (userResource.isLoading()) {
      <p>Loading...</p>
    } @else if (userResource.value(); as user) {
      <h2>{{ user.name }}</h2>
      <p>{{ user.email }}</p>
    }
  `
})
export class UserProfileComponent {
  readonly userId = signal<string>('');

  readonly userResource = resource({
    request: () => ({ id: this.userId() }),
    loader: async ({ request }) => {
      const res = await fetch(`/api/users/${request.id}`);
      return res.json();
    }
  });
}
```

## Template 7: LinkedSignal
```typescript
import { Component, signal, linkedSignal } from '@angular/core';

@Component({
  selector: 'app-tabs',
  standalone: true,
  template: `
    <button (click)="selectTab('overview')">Overview</button>
    <button (click)="selectTab('details')">Details</button>
    <p>Active: {{ activeTab() }}</p>
  `
})
export class TabsComponent {
  readonly userId = signal('');
  readonly activeTab = linkedSignal({
    source: this.userId,
    computation: () => 'overview' // Reseta quando userId muda
  });

  selectTab(tab: string): void {
    this.activeTab.set(tab);
  }
}
```

## Template 8: Bootstrap Configuration
```typescript
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { provideExperimentalZonelessChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideExperimentalZonelessChangeDetection(),
    provideRouter(routes)
  ]
});
```

## Template 9: angular.json (Vitest)
```json
{
  "projects": {
    "my-app": {
      "architect": {
        "test": {
          "builder": "@angular/build:unit-test",
          "options": {
            "vitestConfigFile": "vitest.config.ts"
          }
        }
      }
    }
  }
}
```
