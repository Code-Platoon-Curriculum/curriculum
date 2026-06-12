# How Authentication Works

## <a href="https://docs.google.com/presentation/d/119TXSvkjoYQyb4iRtXXu58Mz9nKILCnCyjyKB36MGr8/edit?usp=drive_link" target="_">LECTURE SLIDE DECK</a>

## Intro

You've built a working full-stack task manager. Users can create tasks, read them, update them, delete them. It works.

But here's the problem: *anyone* can do any of that. There's nothing stopping a random person from reading every user's tasks, deleting records, or pretending to be someone they're not. Your app has no concept of identity.

That's what this lecture is about. Before we implement authentication in the next lecture, you need to understand *what* authentication actually is, *why* it exists, and *how* the different approaches work — so that when Claude Code wires it up for you, you know exactly what's happening under the hood and can make informed decisions when things go wrong.

---

## Lesson

### What is Authentication

**Authentication** is the process of verifying *who someone is*.

When a user submits a username and password, your application asks: "Do I recognize this person? Do their credentials match what I have on record?" If yes — they're authenticated. If no — they're a stranger.

Think of it like a bouncer checking your ID at the door. The bouncer doesn't care what you're going to do inside yet. They just need to confirm you are who you say you are.

In web applications, authentication typically involves:
1. The user presenting some **credential** (password, token, biometric, etc.)
2. The server **verifying** that credential against a trusted source
3. The server issuing some form of **proof** that the user is now recognized (a session, a token, a cookie)

---

### What is Authorization

**Authorization** is the process of verifying *what someone is allowed to do*.

Once your app knows *who* a user is, it still needs to decide: can this particular user read this record? Can they delete it? Are they an admin or a regular user?

Back to the bouncer analogy: authorization is the VIP list inside the venue. You got past the door (authentication), but not everyone gets into the back room (authorization).

In your task manager, authorization would answer questions like:
- Can user A see user B's tasks? *(No — tasks belong to their owner.)*
- Can a regular user delete another user's account? *(No — that's an admin action.)*
- Can a user edit their own profile? *(Yes.)*

---

### Authentication vs Authorization

These two are frequently confused, even by experienced developers. Here's the clearest way to keep them separate:

| | Authentication | Authorization |
|---|---|---|
| **Question** | Who are you? | What can you do? |
| **Happens** | First | Second (auth must come first) |
| **Failure response** | `401 Unauthorized` | `403 Forbidden` |
| **Example** | Logging in with email + password | Checking if you own the task you're trying to delete |

> Note the HTTP status code naming is famously confusing: `401 Unauthorized` actually means *unauthenticated*, and `403 Forbidden` means *unauthorized*. You're not alone if that bothers you.

Authentication is a **prerequisite** for authorization. You can't decide what someone is allowed to do if you don't know who they are.

---

### Types of Authentication

There are several approaches to authentication in web applications. Each has tradeoffs, and understanding them will help you recognize what Supabase is doing — and why.

---

#### Basic Authentication

The simplest possible approach. On every request, the client sends a username and password directly in the HTTP header, encoded in Base64.

```
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

The server decodes it, looks up the user, verifies the password — every single time.

**Pros:**
- Dead simple to implement
- Stateless — no server-side session storage needed

**Cons:**
- Credentials are sent with *every request* — more exposure surface
- Base64 is encoding, not encryption — requires HTTPS to be safe at all
- No concept of "logout" — the client just stops sending credentials
- Terrible user experience for browser-based apps

**Where you'll see it:** Internal tools, simple API access, legacy systems. Not appropriate for modern user-facing web apps.

---

#### Session-Based Authentication

The user logs in once, and the server creates a **session** — a record stored server-side (in memory, a database, or a cache like Redis) that represents "this user is currently logged in." The server sends back a **session ID** in a cookie. On every subsequent request, the browser automatically sends that cookie, and the server looks up the session to identify the user.

```
Browser                        Server
  |                               |
  |-- POST /login (email+pass) -->|
  |                               |--> verify credentials
  |                               |--> create session in DB
  |<-- Set-Cookie: session_id ----|
  |                               |
  |-- GET /tasks (+ cookie) ----->|
  |                               |--> look up session_id
  |                               |--> find user
  |<-- 200 tasks data ------------|
```

**Pros:**
- Easy to invalidate — delete the session server-side and the user is logged out immediately
- Session data stays on the server — the client only holds an opaque ID

**Cons:**
- **Stateful** — the server must store and look up sessions. This gets complicated with multiple servers (which server has the session?)
- Scaling requires shared session storage (Redis, a database), adding infrastructure complexity
- Cookies can be vulnerable to CSRF attacks if not configured carefully

**Where you'll see it:** Traditional server-rendered web apps (Rails, Django, Express with express-session).

---

#### Token-Based Authentication

The user logs in once, and the server issues a **signed token** — most commonly a **JWT (JSON Web Token)**. The token is stored client-side (localStorage or memory) and sent with every request in the `Authorization` header. The server doesn't store the token — it just *verifies the signature* to trust it.

```
Browser                        Server
  |                               |
  |-- POST /login (email+pass) -->|
  |                               |--> verify credentials
  |                               |--> generate signed JWT
  |<-- { token: "eyJ..." } -------|
  |                               |
  |-- GET /tasks                  |
  |   Authorization: Bearer eyJ->|
  |                               |--> verify JWT signature
  |                               |--> decode user from token
  |<-- 200 tasks data ------------|
```

A JWT has three parts — header, payload, signature — separated by dots. The payload contains **claims**: information about the user (their ID, role, expiration time). Because it's *signed* with a secret key, the server can verify it wasn't tampered with — without storing anything.

**Pros:**
- **Stateless** — no server-side storage required. Scales horizontally with no shared state
- Works great for APIs and single-page applications
- Can carry user information (claims) directly in the token

**Cons:**
- **Cannot be invalidated before expiration** — if a token is stolen, it's valid until it expires. You'd need a blocklist to force-invalidate, which reintroduces statefulness
- Token payload is encoded but not encrypted — don't store sensitive data in it
- If stored in localStorage, vulnerable to XSS attacks

**Where you'll see it:** REST APIs, mobile apps, microservices.

---

#### Session + Token-Based Authentication

Many modern systems — including Supabase — use a **hybrid approach** that combines the best of both worlds:

- A **short-lived access token (JWT)** is used for actual API requests. It expires quickly (minutes to hours), limiting the damage window if stolen.
- A **long-lived refresh token** is stored securely (typically in an `httpOnly` cookie, which JavaScript can't read). When the access token expires, the client silently exchanges the refresh token for a new access token.

```
Browser                        Auth Server          API Server
  |                               |                     |
  |-- POST /login --------------->|                     |
  |<-- access_token (JWT, 1hr) ---|                     |
  |    refresh_token (cookie) ----|                     |
  |                               |                     |
  |-- GET /tasks (access_token) ----------------------->|
  |<-- 200 tasks ------------------------------------------------|
  |                               |                     |
  |   [1 hour later]              |                     |
  |                               |                     |
  |-- GET /tasks (expired JWT) ------------------------>|
  |<-- 401 Unauthorized ---------------------------------|
  |                               |                     |
  |-- POST /refresh (cookie) ---->|                     |
  |<-- new access_token -----------|                    |
  |                               |                     |
  |-- GET /tasks (new token) -------------------------->|
  |<-- 200 tasks ------------------------------------------------|
```

**Pros:**
- Short-lived access tokens limit exposure
- Refresh tokens can be rotated and revoked server-side — giving you actual logout capability
- Stateless for the hot path (API requests), stateful only for refresh

**Cons:**
- More complex to implement from scratch
- Refresh token rotation needs careful handling to avoid race conditions
- Still requires secure storage of the refresh token

**Where you'll see it:** Firebase, Auth0, Supabase — essentially all serious modern authentication platforms.

---

#### Choosing the Best Authentication Type for YOUR Application

There's no universally correct answer, but here's a practical framework:

| If your app is... | Consider... |
|---|---|
| A simple internal API or CLI tool | Basic Auth |
| A traditional server-rendered app (minimal JS) | Session-based |
| A React SPA calling a REST API (like yours) | Token-based or Session + Token |
| An app needing true logout / session revocation | Session + Token hybrid |
| A distributed system / microservices | Token-based (stateless scales better) |
| Using an auth platform (Supabase, Firebase, Auth0) | Whatever they provide — it's Session + Token |

For your stack — a Vite + React SPA hitting a Supabase backend — the decision has largely already been made for you. Which brings us to the last section.

---

### What Type of Authentication Does Supabase Provide?

Supabase uses a **Session + Token hybrid** approach, built on top of the open standard **OAuth 2.0** and **JWT**.

Here's specifically what happens when you use Supabase Auth:

1. **Login:** The user submits credentials to Supabase Auth. Supabase verifies them against its `auth.users` table (a separate, managed schema — not your public `users` table).

2. **Token issuance:** Supabase returns two things:
   - An **access token** — a signed JWT, valid for **1 hour** by default. This token contains the user's `sub` (their UUID), their role, and expiration time in its payload.
   - A **refresh token** — a long-lived, opaque string stored in the client via Supabase's JS client library (`@supabase/supabase-js`), typically in localStorage or a cookie depending on configuration.

3. **Authenticated requests:** When your React app calls any Supabase endpoint, `@supabase/supabase-js` automatically attaches the current access token as a Bearer token in the `Authorization` header. PostgREST — the layer sitting in front of your PostgreSQL database — reads that JWT, verifies the signature against Supabase's secret, and exposes the user's identity to your database via `auth.uid()`.

4. **Token refresh:** The Supabase client handles silent token refresh automatically. When the access token is about to expire, it uses the refresh token to get a new one — invisible to the user.

5. **Row-Level Security (RLS):** This is where authentication meets authorization in Supabase. Once the user's identity is established via JWT, you write **RLS policies** in PostgreSQL that use `auth.uid()` to control which rows a user can read, insert, update, or delete. For example:

```sql
-- Users can only see their own tasks
CREATE POLICY "Users can view own tasks"
ON tasks
FOR SELECT
USING (auth.uid() = user_id);
```

This is the full picture: Supabase handles the authentication machinery (tokens, refresh, session management), and PostgreSQL RLS handles authorization (who can touch what data).

---

## Conclusion

Authentication and authorization are the foundation of any application that deals with real users and real data. Before this lecture, your task manager was an open house — anyone could walk in and touch anything. 

Here's what you now understand:

- **Authentication** answers *who are you*, and **authorization** answers *what can you do* — they are sequential, not interchangeable
- **Basic auth** is simple but not suited for SPAs; **session-based** auth works well for traditional apps but doesn't scale easily; **token-based** auth is stateless and scales well but can't be revoked; **session + token hybrid** gives you the best of both
- **Supabase uses a session + token hybrid** — JWTs for stateless API access, refresh tokens for longevity and revocability, and RLS policies for row-level authorization directly in the database

In the next lecture, you'll direct Claude Code to implement Supabase Auth in your application — wiring up signup, login, logout, protected routes on the front end, and RLS policies on the back end. With this foundation, you'll understand every piece of what gets built.