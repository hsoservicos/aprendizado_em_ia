# bmad-php84

PHP 8.4 Architect — Property Hooks, Asymmetric Visibility, DOM API, Array Functions

## Usage

```bash
# Via BMAD render script
uv run _bmad/scripts/render_skill.py --project-root /home/hsantos/app --skill .agents/skills/bmad-php84
```

## Skills Covered

- Property Hooks (get/set)
- Asymmetric Visibility (public private(set))
- New DOM API (HTML5)
- Array Functions (array_find, array_any, array_all)
- Expression Syntax (new Foo()->bar())
- Lazy Objects
- BCMath Object API
- #[\Deprecated] Attribute
- mb_trim/mb_ltrim/mb_rtrim

## Examples

```php
// Property Hooks
public string $name {
    set(string $value) {
        $this->name = strtolower($value);
    }
}

// Asymmetric Visibility
public private(set) float $total = 0.0;

// New Expression Syntax
$result = new MyClass()->doSomething();

// Array Functions
$active = array_any($users, fn($u) => $u['active']);
```
