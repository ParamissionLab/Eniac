# Stack Patterns and Pitfalls

Concrete code examples for common pitfalls and good patterns. Read only the section matching the detected stack. These complement `stack-risk-matrix.md` which covers invariants and proof signals at a higher level.

## Contents

- [TypeScript / Node.js](#typescript--nodejs)
- [Python](#python)
- [Go](#go)
- [Rust](#rust)
- [Zig](#zig)
- [Ruby](#ruby)
- [Java / Kotlin](#java--kotlin)
- [C# / .NET](#c--net)
- [React / Next.js](#react--nextjs)
- [REST API patterns](#rest-api-patterns)
- [Database patterns](#database-patterns)

---

## TypeScript / Node.js

### Setup

```bash
npm init -y
npm install -D typescript @types/node
npx tsc --init
```

### Pitfalls

**1. `any` hides contract drift**

```typescript
// Bad — runtime failure, no compile error
function parse(data: any) {
  return data.user.name.toUpperCase()
}

// Good — validate at boundary
import { z } from 'zod'
const UserSchema = z.object({ user: z.object({ name: z.string() }) })
function parse(data: unknown) {
  const { user } = UserSchema.parse(data)
  return user.name.toUpperCase()
}
```

**2. Floating promises (no await)**

```typescript
// Bad — error silently lost, execution continues
async function save(user: User) {
  db.insert(user) // forgot await
  console.log('saved') // runs before insert completes
}

// Good
async function save(user: User) {
  await db.insert(user)
  console.log('saved')
}
```

**3. Unvalidated environment variables**

```typescript
// Bad — undefined at runtime, discovered in production
const port = process.env.PORT

// Good — fail fast at startup
const port = process.env.PORT
  ? parseInt(process.env.PORT, 10)
  : (() => { throw new Error('PORT env var required') })()
```

**4. Inconsistent module resolution (ESM/CJS)**

```typescript
// Bad — works in dev, breaks in production bundle
import { helper } from './utils' // missing extension in ESM

// Good — explicit for ESM projects
import { helper } from './utils.js'
// Or set "moduleResolution": "bundler" in tsconfig.json
```

### Good Patterns

```typescript
// Result type instead of throw — composable error handling
type Result<T, E = string> =
  | { ok: true; data: T }
  | { ok: false; error: E }

function findUser(id: string): Result<User> {
  const user = db.get(id)
  if (!user) return { ok: false, error: `User ${id} not found` }
  return { ok: true, data: user }
}

// Exhaustive switch check
function handle(status: 'active' | 'inactive' | 'banned'): string {
  switch (status) {
    case 'active': return 'Welcome'
    case 'inactive': return 'Please verify email'
    case 'banned': return 'Account suspended'
    default: {
      const _exhaustive: never = status
      return _exhaustive
    }
  }
}
```

---

## Python

### Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Pitfalls

**1. Mutable default arguments**

```python
# Bad — list shared across all calls
def add_item(item, items=[]):
    items.append(item)
    return items

add_item('a')  # ['a']
add_item('b')  # ['a', 'b'] — surprise!

# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

**2. Broad exception catching**

```python
# Bad — hides bugs, catches KeyboardInterrupt
try:
    result = process(data)
except Exception:
    pass

# Good — specific exceptions, actionable handling
try:
    result = process(data)
except ValueError as e:
    logger.warning(f"Invalid data: {e}")
    result = default_value
except ConnectionError as e:
    raise ServiceUnavailable(f"Backend unreachable: {e}") from e
```

**3. Relative import failures**

```python
# Bad — breaks when running `python src/module.py` directly
from .utils import helper

# Good — run as module: `python -m src.module`
# Or use absolute imports from project root
from src.utils import helper
```

**4. `is` vs `==` confusion**

```python
# Bad — identity check on values (works for small ints by accident)
if x is 256:   # True (cached)
if x is 257:   # False (not cached) — surprise!

# Good — use == for value equality
if x == 257:   # True
# Use `is` ONLY for None/True/False singletons
if result is None:
    handle_missing()
```

### Good Patterns

```python
from dataclasses import dataclass
from typing import Optional

# Dataclass for value objects
@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080
    debug: bool = False

# Context manager for resource cleanup
from contextlib import contextmanager

@contextmanager
def managed_connection(url: str):
    conn = connect(url)
    try:
        yield conn
    finally:
        conn.close()
```

---

## Go

### Setup

```bash
go mod init github.com/user/project
```

### Pitfalls

**1. Ignored errors**

```go
// Bad — silent failure
file, _ := os.Open("config.json")
data, _ := io.ReadAll(file)

// Good — wrap with context
file, err := os.Open("config.json")
if err != nil {
    return fmt.Errorf("opening config: %w", err)
}
defer file.Close()

data, err := io.ReadAll(file)
if err != nil {
    return fmt.Errorf("reading config: %w", err)
}
```

**2. Goroutine leaks**

```go
// Bad — goroutine runs forever if nobody reads ch
func fetch(url string) <-chan string {
    ch := make(chan string)
    go func() {
        resp := httpGet(url)
        ch <- resp // blocks forever if receiver gone
    }()
    return ch
}

// Good — use context for cancellation
func fetch(ctx context.Context, url string) <-chan string {
    ch := make(chan string, 1) // buffered
    go func() {
        resp := httpGet(url)
        select {
        case ch <- resp:
        case <-ctx.Done():
        }
    }()
    return ch
}
```

**3. Nil interface surprise**

```go
// Bad — interface holding typed nil is not == nil
var err *MyError // typed nil
var e error = err
fmt.Println(e == nil) // false!

// Good — return the interface zero value directly
func validate(x int) error {
    if x < 0 {
        return &MyError{msg: "negative"}
    }
    return nil // not a typed nil pointer
}
```

### Good Patterns

```go
// Table-driven tests
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"zero", 0, 0, 0},
        {"negative", -1, 1, 0},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := Add(tt.a, tt.b); got != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.expected)
            }
        })
    }
}

// Functional options pattern
type ServerOption func(*Server)

func WithPort(port int) ServerOption {
    return func(s *Server) { s.port = port }
}

func NewServer(opts ...ServerOption) *Server {
    s := &Server{port: 8080} // sensible default
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

---

## Rust

### Setup

```bash
cargo new project-name
cd project-name
```

### Pitfalls

**1. `unwrap()` in production code**

```rust
// Bad — panics on None/Err
let config = std::fs::read_to_string("config.toml").unwrap();

// Good — propagate with ?
fn load_config() -> Result<String, std::io::Error> {
    let config = std::fs::read_to_string("config.toml")?;
    Ok(config)
}
```

**2. Clone-everywhere hiding design issues**

```rust
// Bad — excessive cloning to fight borrow checker
fn process(data: &Vec<String>) -> Vec<String> {
    let mut result = data.clone(); // unnecessary
    result.sort();
    result
}

// Good — take ownership or borrow correctly
fn process(mut data: Vec<String>) -> Vec<String> {
    data.sort();
    data
}
```

**3. Blocking in async context**

```rust
// Bad — blocks the async runtime thread
async fn read_file() -> String {
    std::fs::read_to_string("data.txt").unwrap() // sync I/O in async!
}

// Good — use async file I/O
async fn read_file() -> Result<String, std::io::Error> {
    tokio::fs::read_to_string("data.txt").await
}
```

### Good Patterns

```rust
// Custom error type with thiserror
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("invalid input: {0}")]
    Validation(String),
}

// Builder pattern
pub struct RequestBuilder {
    url: String,
    timeout: Option<Duration>,
    headers: Vec<(String, String)>,
}

impl RequestBuilder {
    pub fn new(url: impl Into<String>) -> Self {
        Self { url: url.into(), timeout: None, headers: vec![] }
    }
    pub fn timeout(mut self, d: Duration) -> Self { self.timeout = Some(d); self }
    pub fn header(mut self, k: impl Into<String>, v: impl Into<String>) -> Self {
        self.headers.push((k.into(), v.into())); self
    }
    pub fn build(self) -> Request { /* ... */ }
}
```

---

## Zig

### Setup

```bash
# Download from https://ziglang.org/download/ or use package manager
# Project with build system:
mkdir project && cd project
zig init
# Creates build.zig + src/main.zig + src/root.zig
```

### Pitfalls

**1. Undefined behavior from `@intCast` without bounds check**

```zig
// Bad — undefined behavior if value overflows target type
const big: u64 = 300;
const small: u8 = @intCast(big); // UB! 300 > 255

// Good — check or use saturating/wrapping arithmetic
const big: u64 = 300;
const small: u8 = std.math.cast(u8, big) orelse {
    return error.Overflow;
};
// Or use saturating cast when truncation is acceptable:
const clamped: u8 = @truncate(big); // explicit intent
```

**2. Forgetting to handle error unions**

```zig
// Bad — discarding error silently
const file = std.fs.cwd().openFile("config.txt", .{}) catch unreachable;
// crashes in production if file doesn't exist

// Good — propagate or handle explicitly
const file = std.fs.cwd().openFile("config.txt", .{}) catch |err| {
    std.log.err("Failed to open config: {}", .{err});
    return err;
};
defer file.close();
```

**3. Use-after-free with slices from temporary allocations**

```zig
// Bad — slice points to freed memory
fn getBuffer(allocator: std.mem.Allocator) ![]u8 {
    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit(); // frees the underlying memory!
    try list.appendSlice("hello");
    return list.items; // dangling pointer!
}

// Good — transfer ownership, let caller free
fn getBuffer(allocator: std.mem.Allocator) !std.ArrayList(u8) {
    var list = std.ArrayList(u8).init(allocator);
    try list.appendSlice("hello");
    return list; // caller owns and calls deinit()
}
// Or use toOwnedSlice:
fn getBuffer(allocator: std.mem.Allocator) ![]u8 {
    var list = std.ArrayList(u8).init(allocator);
    defer list.deinit();
    try list.appendSlice("hello");
    return try list.toOwnedSlice(); // caller frees with allocator.free()
}
```

**4. Ignoring allocator failures**

```zig
// Bad — catch unreachable on allocation (OOM = crash)
const buf = allocator.alloc(u8, size) catch unreachable;

// Good — propagate allocation errors
const buf = try allocator.alloc(u8, size);
defer allocator.free(buf);
```

**5. Sentinel-terminated vs regular slices confusion**

```zig
// Bad — passing regular slice where sentinel-terminated expected
const data: []const u8 = &[_]u8{ 'h', 'i' };
const c_str: [*:0]const u8 = data; // compile error!

// Good — use sentinel-terminated literal or explicitly add sentinel
const c_str: [:0]const u8 = "hi"; // string literals are null-terminated
// Or for dynamic data:
const c_str = try allocator.dupeZ(u8, data); // appends null sentinel
defer allocator.free(c_str);
```

### Good Patterns

```zig
// Comptime generics — type-safe generic data structure
fn BoundedArray(comptime T: type, comptime capacity: usize) type {
    return struct {
        buffer: [capacity]T = undefined,
        len: usize = 0,

        const Self = @This();

        pub fn append(self: *Self, item: T) !void {
            if (self.len >= capacity) return error.Overflow;
            self.buffer[self.len] = item;
            self.len += 1;
        }

        pub fn slice(self: *const Self) []const T {
            return self.buffer[0..self.len];
        }
    };
}

// Defer for cleanup (RAII equivalent)
fn processFile(path: []const u8) !void {
    const file = try std.fs.cwd().openFile(path, .{});
    defer file.close();

    var buf_reader = std.io.bufferedReader(file.reader());
    // file automatically closed when function returns (success or error)
}

// Tagged union for sum types (like Rust enum)
const Token = union(enum) {
    number: f64,
    identifier: []const u8,
    plus,
    eof,

    pub fn format(self: Token) []const u8 {
        return switch (self) {
            .number => |n| std.fmt.allocPrint(allocator, "{d}", .{n}),
            .identifier => |id| id,
            .plus => "+",
            .eof => "EOF",
        };
    }
};

// Testing with std.testing
test "addition works" {
    const result = add(2, 3);
    try std.testing.expectEqual(@as(i32, 5), result);
}

test "allocation failure handled" {
    const failing_allocator = std.testing.failing_allocator;
    const result = createBuffer(failing_allocator, 100);
    try std.testing.expectError(error.OutOfMemory, result);
}
```

---

## Ruby

### Setup

```bash
bundle install
```

### Pitfalls

**1. N+1 queries in ActiveRecord**

```ruby
# Bad — one query per post for author
Post.all.each { |p| puts p.author.name }
# SELECT * FROM posts
# SELECT * FROM authors WHERE id = 1  (repeated N times)

# Good — eager load
Post.includes(:author).each { |p| puts p.author.name }
# SELECT * FROM posts
# SELECT * FROM authors WHERE id IN (1, 2, 3, ...)
```

**2. Nil propagation hiding bugs**

```ruby
# Bad — returns nil silently, error surfaces far from cause
user = User.find_by(id: params[:id])
user.profile.avatar_url  # NoMethodError on nil, but where?

# Good — fail fast or use safe navigation intentionally
user = User.find_by!(id: params[:id])  # raises RecordNotFound
# Or with explicit nil handling:
user&.profile&.avatar_url || default_avatar
```

**3. Monkey-patching core classes**

```ruby
# Bad — affects all String instances globally
class String
  def to_slug
    downcase.gsub(/\s+/, '-')
  end
end

# Good — use refinements (scoped)
module SlugSupport
  refine String do
    def to_slug
      downcase.gsub(/\s+/, '-')
    end
  end
end
# Then: using SlugSupport in the file that needs it
```

### Good Patterns

```ruby
# Struct for value objects (immutable-ish, with named fields)
User = Struct.new(:name, :email, keyword_init: true)
user = User.new(name: "Ada", email: "ada@example.com")

# Service object pattern
class CreateOrder
  def initialize(user:, cart:)
    @user = user
    @cart = cart
  end

  def call
    validate!
    order = Order.create!(user: @user, items: @cart.items)
    PaymentService.charge(@user, order.total)
    OrderMailer.confirmation(order).deliver_later
    order
  end

  private

  def validate!
    raise ArgumentError, "Empty cart" if @cart.empty?
  end
end
```

---

## Java / Kotlin

### Setup

```bash
# Gradle
gradle init --type java-application

# Maven
mvn archetype:generate -DgroupId=com.example -DartifactId=my-app
```

### Pitfalls

**1. NullPointerException**

```java
// Bad — null returned, discovered at call site
public User findUser(long id) {
    return userRepository.findOne(id); // might be null
}

// Good — Optional makes null handling explicit
public Optional<User> findUser(long id) {
    return Optional.ofNullable(userRepository.findOne(id));
}

// Caller must handle it:
findUser(42).orElseThrow(() -> new NotFoundException("User 42"));
```

**2. Resource leaks**

```java
// Bad — connection not closed on exception
Connection conn = dataSource.getConnection();
PreparedStatement ps = conn.prepareStatement(sql);
ResultSet rs = ps.executeQuery();
// if exception here, resources leak

// Good — try-with-resources (auto-close)
try (Connection conn = dataSource.getConnection();
     PreparedStatement ps = conn.prepareStatement(sql);
     ResultSet rs = ps.executeQuery()) {
    while (rs.next()) {
        process(rs);
    }
}
```

**3. String concatenation in loops**

```java
// Bad — O(n²) memory allocation
String result = "";
for (String item : items) {
    result += item + ", "; // new String each iteration
}

// Good
String result = String.join(", ", items);
// Or StringBuilder for complex cases
```

### Good Patterns

```java
// Record types (Java 16+) for immutable data
public record User(long id, String name, String email) {}

// Sealed interfaces for exhaustive pattern matching (Java 17+)
public sealed interface Shape permits Circle, Rectangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double w, double h) implements Shape {}

double area(Shape s) {
    return switch (s) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
    };
}
```

---

## C# / .NET

### Setup

```bash
dotnet new console -n MyApp
cd MyApp
```

### Pitfalls

**1. `async void` causes unhandled exceptions**

```csharp
// Bad — exceptions crash the process, can't be awaited
async void ProcessData() {
    await LoadAsync(); // if this throws, app crashes
}

// Good — always return Task
async Task ProcessDataAsync() {
    await LoadAsync(); // caller can catch exceptions
}
```

**2. Sync-over-async deadlock**

```csharp
// Bad — deadlocks in ASP.NET (pre-.NET 6) or UI apps
public string GetData() {
    return GetDataAsync().Result; // blocks, deadlock!
}

// Good — async all the way
public async Task<string> GetDataAsync() {
    var data = await _httpClient.GetStringAsync(url)
        .ConfigureAwait(false);
    return data;
}
```

**3. Multiple enumeration of IEnumerable**

```csharp
// Bad — query executes twice
IEnumerable<User> users = db.Users.Where(u => u.Active);
var count = users.Count();      // query 1
var list = users.ToList();      // query 2

// Good — materialize once
var users = db.Users.Where(u => u.Active).ToList();
var count = users.Count;  // in-memory, no extra query
```

### Good Patterns

```csharp
// Record types for immutable DTOs (C# 9+)
public record UserDto(int Id, string Name, string Email);

// Result pattern without exceptions
public class Result<T> {
    public bool IsSuccess { get; }
    public T? Value { get; }
    public string? Error { get; }

    private Result(T value) { IsSuccess = true; Value = value; }
    private Result(string error) { IsSuccess = false; Error = error; }

    public static Result<T> Ok(T value) => new(value);
    public static Result<T> Fail(string error) => new(error);
}
```

---

## React / Next.js

### Pitfalls

**1. Missing `key` prop causes re-render bugs**

```tsx
// Bad — index as key breaks on reorder/delete
{items.map((item, i) => <Item key={i} data={item} />)}

// Good — stable unique identifier
{items.map(item => <Item key={item.id} data={item} />)}
```

**2. Stale closure in useEffect**

```tsx
// Bad — count is captured at 0, never updates
useEffect(() => {
  const id = setInterval(() => {
    setCount(count + 1) // always 0 + 1
  }, 1000)
  return () => clearInterval(id)
}, []) // empty deps = stale closure

// Good — use functional updater
useEffect(() => {
  const id = setInterval(() => {
    setCount(prev => prev + 1)
  }, 1000)
  return () => clearInterval(id)
}, [])
```

**3. Race condition on fast navigation**

```tsx
// Bad — response from old request overwrites new data
useEffect(() => {
  fetchUser(userId).then(setUser)
}, [userId])

// Good — cleanup with abort flag
useEffect(() => {
  let cancelled = false
  fetchUser(userId).then(data => {
    if (!cancelled) setUser(data)
  })
  return () => { cancelled = true }
}, [userId])
```

**4. Server/client boundary leakage (Next.js App Router)**

```tsx
// Bad — secret leaks to client bundle
// app/page.tsx (Server Component)
const API_KEY = process.env.SECRET_KEY
// If imported into a Client Component, it's bundled!

// Good — keep secrets in server-only code
// lib/api.server.ts
import 'server-only'
export async function fetchData() {
  return fetch(url, { headers: { Authorization: process.env.SECRET_KEY! } })
}
```

### Good Patterns

```tsx
// Custom hook for data fetching
function useUser(id: string) {
  const [state, setState] = useState<{
    user: User | null
    loading: boolean
    error: string | null
  }>({ user: null, loading: true, error: null })

  useEffect(() => {
    let cancelled = false
    setState(s => ({ ...s, loading: true, error: null }))
    fetchUser(id)
      .then(user => !cancelled && setState({ user, loading: false, error: null }))
      .catch(e => !cancelled && setState({ user: null, loading: false, error: e.message }))
    return () => { cancelled = true }
  }, [id])

  return state
}
```

---

## REST API Patterns

### Input Validation (any framework)

```typescript
// Bad — trusting request body directly
app.post('/users', (req, res) => {
  db.insert(req.body) // SQL injection, invalid data, etc.
})

// Good — validate at boundary
import { z } from 'zod'
const CreateUser = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(128),
  name: z.string().min(1).max(100),
})

app.post('/users', (req, res) => {
  const parsed = CreateUser.safeParse(req.body)
  if (!parsed.success) {
    return res.status(400).json({ errors: parsed.error.flatten().fieldErrors })
  }
  db.insert(parsed.data) // typed and validated
})
```

### Error Response Shape

```typescript
// Bad — leaks stack trace to client
app.use((err, req, res, next) => {
  res.status(500).json({ error: err.stack })
})

// Good — structured, safe error response
app.use((err, req, res, next) => {
  const status = err.statusCode || 500
  const message = status === 500 ? 'Internal server error' : err.message
  logger.error({ err, requestId: req.id }) // full details in logs only
  res.status(status).json({ error: { message, code: err.code, requestId: req.id } })
})
```

---

## Database Patterns

### N+1 Query Detection

```python
# Bad — one query per iteration
for order in Order.objects.all():
    print(order.customer.name)  # separate SELECT each time

# Good — prefetch related
for order in Order.objects.select_related('customer').all():
    print(order.customer.name)  # single JOIN query
```

### Index Strategy

```sql
-- Add indexes on: foreign keys, columns in WHERE/ORDER BY, unique constraints
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_status_created ON orders(status, created_at);

-- Verify with EXPLAIN
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at;
```

### Transaction Safety

```python
# Bad — partial write on failure
def transfer(from_id, to_id, amount):
    debit(from_id, amount)   # succeeds
    credit(to_id, amount)    # fails — money vanished!

# Good — atomic transaction
from django.db import transaction

@transaction.atomic
def transfer(from_id, to_id, amount):
    debit(from_id, amount)
    credit(to_id, amount)
    # both succeed or both rollback
```
