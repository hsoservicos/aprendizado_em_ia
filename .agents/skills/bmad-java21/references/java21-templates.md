# Java 21 LTS — Templates de Código

## Template 1: Virtual Threads + Structured Concurrency
```java
public record UserSummary(String userId, String profileName, List<Order> orders) {}

public class UserAggregatorService {

    public UserSummary fetchUserSummary(String userId)
            throws InterruptedException, ExecutionException {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Supplier<String> profileTask = scope.fork(() -> fetchProfileName(userId));
            Supplier<List<Order>> ordersTask = scope.fork(() -> fetchUserOrders(userId));

            scope.join();
            scope.throwIfFailed();

            return new UserSummary(userId, profileTask.get(), ordersTask.get());
        }
    }
}
```

## Template 2: Pattern Matching + Sealed Interface
```java
public sealed interface DomainEvent permits PaymentReceived, OrderCancelled {}
public record PaymentReceived(String orderId, double amount, String currency)
        implements DomainEvent {}
public record OrderCancelled(String orderId, String reason)
        implements DomainEvent {}

public class EventProcessor {

    public String processEvent(DomainEvent event) {
        return switch (event) {
            case PaymentReceived(var orderId, var amount, var currency)
                    when amount > 10_000 ->
                "ALERTA: Pagamento de alto valor: " + orderId;
            case PaymentReceived(var orderId, var amount, var currency) ->
                "Pagamento processado: " + orderId + ": " + amount + " " + currency;
            case OrderCancelled(var orderId, var reason) ->
                "Cancelamento registrado: " + orderId + ". Motivo: " + reason;
        };
    }
}
```

## Template 3: Sequenced Collections
```java
SequencedCollection<String> names = new ArrayList<>();
names.addFirst("Alice");
names.addLast("Bob");
String first = names.getFirst();   // "Alice"
String last = names.getLast();     // "Bob"

for (String name : names.reversed()) {
    System.out.println(name);      // Bob, Alice
}
```

## Template 4: ScopedValue (JEP 446)
```java
private static final ScopedValue<UserContext> CURRENT_USER = ScopedValue.newInstance();

public void processRequest(UserContext user) {
    ScopedValue.runWhere(CURRENT_USER, user, () -> {
        handleRequest();
    });
}

private void handleRequest() {
    UserContext user = CURRENT_USER.get();
    // Processa com contexto do usuário
}
```

## Template 5: REST API com Record
```java
public record ProductRequest(String name, BigDecimal price, String category) {
    public ProductRequest {
        Objects.requireNonNull(name, "name must not be null");
        Objects.requireNonNull(price, "price must not be null");
        if (price.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("price must be positive");
        }
    }
}

public record ProductResponse(String id, String name, BigDecimal price) {}

@RestController
@RequestMapping("/api/products")
public class ProductController {

    @PostMapping
    public ResponseEntity<ProductResponse> create(@RequestBody ProductRequest request) {
        // ...
        return ResponseEntity.ok(response);
    }
}
```

## Template 6: ReentrantLock (anti-pinning)
```java
// ❌ EVITAR: synchronized + I/O causa pinning
public synchronized String fetchData() {
    return httpClient.get(url).body(); // PINNING!
}

// ✅ PREFERIR: ReentrantLock + I/O
private final ReentrantLock lock = new ReentrantLock();

public String fetchData() {
    lock.lock();
    try {
        return httpClient.get(url).body(); // Sem pinning
    } finally {
        lock.unlock();
    }
}
```

## Template 7: Record Patterns aninhados
```java
public record Address(String street, String city) {}
public record Person(String name, Address address) {}
public record Company(String name, Person ceo) {}

// Destruturação aninhada
if (obj instanceof Company(var companyName, Person(var ceoName, Address(var street, var city)))) {
    System.out.println(ceoName + " leads " + companyName + " in " + city);
}
```

## Template 8: Spring Boot + Virtual Threads
```properties
# application.properties
spring.threads.virtual.enabled=true
spring.main.lazy-initialization=false
```

```java
@Service
public class OrderService {

    private final ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

    public CompletableFuture<OrderSummary> processOrder(Order order) {
        return CompletableFuture.supplyAsync(() -> {
            validateOrder(order);
            reserveInventory(order);
            processPayment(order);
            return new OrderSummary(order.id(), "COMPLETED");
        }, executor);
    }
}
```
