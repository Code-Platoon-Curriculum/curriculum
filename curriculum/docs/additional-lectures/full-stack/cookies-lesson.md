# HTTP Cookies

## TLOs (Terminal Learning Objectives)

- Implement cookie-based authentication and session management in web applications
- Apply security best practices to protect cookies from common vulnerabilities
- Choose the appropriate storage mechanism (cookies vs localStorage vs sessionStorage) for different use cases

## ELOs (Enabling Learning Objectives)

- Understand how cookies are transmitted between browser and server
- Set and read cookies from both server-side and client-side code
- Identify and use essential cookie attributes (HttpOnly, Secure, Max-Age, Path)
- Differentiate between session cookies and persistent cookies
- Implement common cookie use cases (authentication, preferences, shopping cart)
- Recognize security vulnerabilities (XSS, CSRF) and apply appropriate mitigations
- Compare cookie-based authentication with token-based authentication

## What are Cookies?

**Cookies** are small pieces of data that websites store on your browser. They help websites remember information about your visit, like login status, preferences, or items in a shopping cart.

## How Cookies Work

When you visit a website, the server can send cookies to your browser through HTTP headers. Your browser stores these cookies and sends them back with every request to that same server.

```mermaid
sequenceDiagram
    participant B as Browser
    participant S as Server
    
    Note over B: User visits website
    B->>S: GET /login<br/>No cookies yet
    S->>B: 200 OK<br/>Set-Cookie: session_id=abc123 🍪
    Note over B: Browser stores cookie 🍪
    
    Note over B: User navigates to profile
    B->>S: GET /profile<br/>Cookie: session_id=abc123 🍪
    Note over S: Server recognizes user
    S->>B: 200 OK<br/>Welcome back, User!
    
    Note over B: Every future request
    B->>S: Any request<br/>Cookie: session_id=abc123 🍪
    S->>B: Response<br/>(May set new cookies)
```

### Setting Cookies from the Server

Here's how servers set cookies (Python examples assume Flask and standard libraries are imported):

```python
@app.route('/login')
def login():
    response = make_response("Welcome back!")
    response.set_cookie('user_id', '12345', max_age=3600)  # Expires in 1 hour
    return response

@app.route('/profile')
def profile():
    user_id = request.cookies.get('user_id')
    if user_id:
        return f"Your user ID is {user_id}"
    return "Please login first"
```

When handling sensitive data, always use security attributes:

```python
response.set_cookie(
    'session_id',
    'abc123',
    max_age=3600,
    secure=True,      # HTTPS only
    httponly=True     # No JavaScript access
)
```

**Note:** These examples are simplified for learning. Production applications require additional security measures.

### Setting Cookies from JavaScript

```javascript
// Setting a cookie with expiration date
const date = new Date();
date.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000)); // 1 year from now
document.cookie = `username=john_doe; expires=${date.toUTCString()}; path=/`;

// Alternative using max-age (in seconds) - cleaner approach
document.cookie = "username=john_doe; max-age=31536000; path=/"; // 1 year

// Reading all cookies
const cookies = document.cookie.split(';');

// Function to get a specific cookie
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(';').shift();
    }
    return null;
}

// How to "delete" a cookie (you're actually expiring it)
// IMPORTANT: path must match exactly how the cookie was set
function deleteCookie(name, path = '/') {
    // This sets the cookie's max-age to 0, causing immediate expiration
    document.cookie = `${name}=; max-age=0; path=${path}`;
}

// Example usage
setCookie('theme', 'dark', 7);        // Set theme for 7 days
console.log(getCookie('theme'));      // "dark"
deleteCookie('theme');                 // Delete it

// Simple helper to set cookies with days
function setCookie(name, value, days) {
    const maxAge = days * 24 * 60 * 60; // Convert days to seconds
    document.cookie = `${name}=${value}; max-age=${maxAge}; path=/`;
}
```

**Important Cookie Deletion Facts:**
- JavaScript can't directly delete cookies - it expires them by setting `max-age=0` or an past `expires` date
- You must use the exact same `path` (and `domain` if set) that was used when creating the cookie
- If you don't know the original path/domain, you can't delete the cookie from JavaScript

**In Production:** Use a library like [js-cookie](https://github.com/js-cookie/js-cookie) or handle cookie deletion server-side for reliability:

```javascript
// With js-cookie library (recommended)
Cookies.set('name', 'value', { expires: 7 });
Cookies.remove('name'); // Library handles the path/domain for you
```

## Essential Cookie Attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| **Name/Value** | The actual data stored | `user_id=12345` |
| **Max-Age** | Seconds until cookie expires | `max_age=3600` (1 hour) |
| **Path** | Which pages can access the cookie | `path=/` (entire site) |
| **Secure** | Only send over HTTPS | `secure=True` |
| **HttpOnly** | Can't be accessed by JavaScript | `httponly=True` |

**Note:** There are other attributes like Domain and SameSite, but these five are the most commonly used.

### Secure Cookie Example

When handling sensitive data, always use security attributes:

```python
response.set_cookie(
    'session_id',     # Cookie name
    'abc123',         # Cookie value
    max_age=3600,     # Cookie TTL (Time To Live) / Expiration
    secure=True,.     # HTTPS only
    httponly=True     # No JavaScript access
)
```

- `max_age` to set when the cookie expires.
- `secure=True` to enforce https so sensitive data is encrypted
- `httponly=True` so that if the website JS code has been hacked the malicious JS cannot access the cookie.

## Types of Cookies

### Session Cookies

- Temporary cookies deleted when browser closes
- No expiration date set
- Used for temporary session data

```python
# Session cookie (no expiration)
response.set_cookie('session_id', 'abc123')
```

### Persistent Cookies

- Have an expiration date
- Stay until expired or manually deleted
- Used for long-term preferences

```python
# Persistent cookie (30 days)
response.set_cookie('remember_me', 'true', max_age=60*60*24*30)
```

## Common Use Cases

### 1. Authentication

Keep users logged in:

```python
@app.route('/login', methods=['POST'])
def login():
    # Assume verify_credentials() returned True
    response = make_response(redirect('/dashboard'))
    response.set_cookie(
        'session_token',         # Cookie name is 'session_token'
        'generated_token_here',  # Cookie value set to the auth token
        max_age=60*60*24,        # Cookie expiration is 24 hours
        httponly=True,           # No JS access
        secure=True              # HTTPS only
    )
    return response

@app.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('session_token', '', max_age=0)  # Delete cookie
    return response
```

### 2. User Preferences
Remember user settings:

```javascript
// Save theme preference
function setTheme(theme) {
    document.cookie = `theme=${theme}; max-age=31536000; path=/`;
    applyTheme(theme);
}

// Load theme on page load
window.onload = function() {
    const theme = getCookie('theme') || 'light';
    applyTheme(theme);
}
```

### 3. Shopping Cart
Store cart items between visits:

```python
@app.route('/add-to-cart/<item_id>')
def add_to_cart(item_id):
    cart_cookie = request.cookies.get('cart')
    
    # Parse existing cart or create new
    try:
        cart = json.loads(cart_cookie) if cart_cookie else []
    except json.JSONDecodeError:
        cart = []
    
    cart.append(item_id)
    
    response = make_response(redirect('/cart'))
    response.set_cookie('cart', json.dumps(cart), max_age=60*60*24*7)
    return response
```

## Security Considerations

### Key Security Attributes

**HttpOnly:** Prevents JavaScript access, protecting against XSS attacks
```python
response.set_cookie('auth_token', token, httponly=True)
```

**Secure:** Ensures cookies are only sent over HTTPS
```python
response.set_cookie('sensitive_data', value, secure=True)
```

**SameSite:** Protects against CSRF attacks
```python
# Strict - Never sent with cross-site requests
response.set_cookie('csrf_token', token, samesite='Strict')

# Lax - Sent with top-level navigation (default in modern browsers)
response.set_cookie('session', session_id, samesite='Lax')
```

**Remember:** Never store passwords or unencrypted sensitive data in cookies!

## Authentication: Cookies vs Authorization Headers

Modern web apps use two main approaches for authentication:

### Cookie-Based Authentication
Server stores a session ID in a cookie:
```python
response.set_cookie('session_id', 'abc123', httponly=True, secure=True)
```
- ✅ Browser automatically sends with every request
- ✅ Can use HttpOnly (prevents JavaScript access)
- ❌ Vulnerable to CSRF attacks
- ❌ Only works on same domain

### Token-Based Authentication
Client sends a token in the Authorization header:
```javascript
// Client must manually add to each request
fetch('/api/data', {
    headers: {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIs...'
    }
})
```
- ✅ Not vulnerable to CSRF (not automatic)
- ✅ Works across different domains
- ❌ Must manually add to every request
- ❌ Need to store token somewhere (localStorage or memory)

### Which Should You Use?

**Use Cookies for:**
- Traditional web applications
- Server-rendered pages (Django, Flask, Rails)
- Simple authentication needs

**Use Authorization Headers for:**
- Single Page Applications (React, Vue)
- Mobile applications
- APIs that serve multiple clients

**Note:** HTTP Basic Auth (sending username:password) exists but is outdated - avoid it in production.

## Cookies vs Other Storage Methods

| Feature | Cookies | localStorage | sessionStorage |
|---------|---------|--------------|----------------|
| **Size Limit** | 4KB | 5-10MB | 5-10MB |
| **Sent to Server** | Yes, with every request | No | No |
| **Expiration** | Configurable | Never (until cleared) | When tab closes |
| **Access** | Server & Client | Client only | Client only |
| **Scope** | Domain/Path specific | Origin specific | Tab specific |
| **Use Case** | Auth, server needs | Large client data | Temporary tab data |

### When to Use Each

**Use Cookies when:**
- Server needs the data (authentication tokens, session IDs)
- Need automatic expiration
- Supporting older browsers

**Use localStorage when:**
- Storing large amounts of client-side data
- Data only needed by JavaScript
- Building offline-capable apps

**Use sessionStorage when:**
- Data should not persist between tabs
- Storing temporary form data

**Avoid Cookies when:**
- Data is only needed client-side (unnecessary server overhead)
- You need complex data structures (cookies only store strings)

## Best Practices

1. **Use HTTPS** - Always set `Secure` flag in production
2. **Set HttpOnly** - For authentication cookies that don't need JavaScript access
3. **Keep cookies small** - Stay under the 4KB limit
4. **Set appropriate expiration** - Don't keep cookies longer than necessary
5. **Use consistent paths** - Usually just use `path=/` for simplicity
6. **Consider alternatives** - Use localStorage for large client-only data

## Quiz

1. **What is the maximum size of a single cookie?**
   - a) 1KB
   - b) 4KB
   - c) 10MB
   - d) Unlimited

2. **Which cookie attribute prevents JavaScript from accessing the cookie?**
   - a) Secure
   - b) SameSite
   - c) HttpOnly
   - d) Path

3. **When are session cookies deleted?**
   - a) After 30 days
   - b) When the browser closes
   - c) Never
   - d) After 1 hour

4. **What happens to an existing cookie when you set it again with max_age=0?**
   - a) Cookie never expires
   - b) Cookie expires in 1 second
   - c) Cookie is deleted immediately
   - d) Cookie becomes a session cookie

**Answers:** 1-b, 2-c, 3-b, 4-c

## Additional Resources

- [MDN HTTP Cookies Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [Web Storage API Guide](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API)
- [js-cookie Library](https://github.com/js-cookie/js-cookie) - Recommended for production use