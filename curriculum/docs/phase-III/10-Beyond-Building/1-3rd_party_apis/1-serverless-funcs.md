# Serverless Functions

## Intro

You've already seen how Supabase gives you a database and auto-generated REST endpoints for your tables. But what happens when you need your backend to *do something* — call an external API, run custom logic, or perform an action that a simple database query can't handle?

That's where **serverless functions** come in. By the end of this lecture, you'll understand what they are, why they exist, and how to deploy your own using Supabase Edge Functions.

---

## Lesson

### Serverless Functions

#### What are Serverless Functions?

A serverless function is a **single piece of backend logic that runs on demand** — triggered by an HTTP request — without you managing any server infrastructure.

Think of it like this: a traditional server is a restaurant kitchen that's running 24/7 whether customers are there or not. A serverless function is a food truck that shows up, makes your order, and drives away.

Under the hood, each function is a small program that:
1. Receives an HTTP request
2. Executes its logic (query a DB, call an API, do math, etc.)
3. Returns an HTTP response
4. Shuts down

The cloud provider (in our case, Supabase via Deno Deploy) handles spinning it up and down. You just write the logic.

**Supabase Edge Functions** specifically run on the **Deno** runtime — a modern, secure alternative to Node.js — and are deployed to servers geographically close to your users for low latency.

---

#### Why Serverless Functions?

Your Supabase project's auto-generated PostgREST endpoints are powerful, but they only talk to *your database*. Serverless functions solve the problems PostgREST can't:

| Need | PostgREST | Edge Function |
|---|---|---|
| Query your database | ✅ | ✅ |
| Call an external API (PokéAPI, Stripe, OpenAI) | ❌ | ✅ |
| Hide secret API keys from the frontend | ❌ | ✅ |
| Run custom business logic before/after a DB write | ❌ | ✅ |
| Send emails or webhooks | ❌ | ✅ |

The most important reason for AI Builders: **your frontend should never hold secret keys**. If you call OpenAI or Stripe directly from React, your API key is visible to anyone who opens DevTools. An Edge Function acts as a secure middleman — your frontend calls *your* function, and your function calls the external service with the secret key safely stored on the server side.

---

#### When to Utilize Serverless Functions

Use a serverless function when you need to:

- **Call a third-party API** — PokéAPI, OpenAI, weather services, payment processors, etc.
- **Protect secret credentials** — API keys, tokens, or secrets that must never reach the browser
- **Perform logic not expressible as a DB query** — transforming data, aggregating from multiple sources, running algorithms
- **Trigger side effects** — sending an email on user signup, posting to Slack, logging to an analytics service

You do *not* need a serverless function for:
- Standard CRUD on your own tables (use PostgREST)
- Client-side computations (do it in React)

---

### CORS

#### What is CORS

When your React app running on `localhost:5173` makes a request to your Supabase Edge Function running on a completely different domain, the browser doesn't just allow that automatically. **CORS — Cross-Origin Resource Sharing** — is the security mechanism that controls whether that request is permitted.

An "origin" is the combination of protocol, domain, and port. These are all different origins:

| Origin | Different Because |
|---|---|
| `http://localhost:5173` | your Vite dev server |
| `https://yourapp.com` | your production frontend |
| `https://xyz.supabase.co` | your Edge Function |

When your frontend makes a request to a *different* origin, the browser first checks whether the server explicitly allows it. If the server doesn't respond with the right headers saying "yes, this origin is permitted," the browser **blocks the response** — even if the server processed the request successfully. This is a browser-enforced rule, not a server rule.

The server signals permission through response headers, the most important being:

```
Access-Control-Allow-Origin: *
```

This tells the browser: "any origin is allowed to read this response." You can also lock it down to a specific origin instead of the wildcard `*`.

**The preflight request** adds one more wrinkle. For certain request types (anything with a custom header like `Authorization`, or a `Content-Type` of `application/json`), the browser sends a preliminary `OPTIONS` request *before* your real request — essentially asking the server "are you going to allow this?" Your Edge Function must respond to that `OPTIONS` request correctly or the real request never goes through.

---

#### How & When to Account for CORS

**When:** Any time your Edge Function will be called from a browser. If the function is only ever called server-to-server, CORS doesn't apply — it's purely a browser enforcement mechanism. Since your frontend is a React app running in the browser, you will need CORS headers on every Edge Function you build.

**How:** Two things need to happen in every Edge Function:

**1. Handle the preflight `OPTIONS` request:**

```typescript
if (req.method === "OPTIONS") {
  return new Response("ok", { headers: corsHeaders });
}
```

**2. Include CORS headers on every response you return:**

```typescript
const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

return new Response(JSON.stringify(data), {
  headers: { ...corsHeaders, "Content-Type": "application/json" },
});
```

Note that the CORS headers must be spread onto *every* response — including error responses. A function that returns a 500 error without CORS headers will still get blocked by the browser, and you'll see a CORS error in DevTools instead of the actual error message, which makes debugging painful.

The good news: when prompting Claude Code to create an Edge Function, simply stating **"include proper CORS headers so this function can be called from a browser"** is enough — it knows the pattern. You just need to understand why it's there so you can recognize a CORS error when you see one and know it's a header problem, not a logic problem.

---

### Implementing an Edge Function w/ Supabase

> The following sections provide prompts to give Claude Code. Your Supabase CLI is already installed, authenticated, and linked to your project.

---

#### Hello World Function

```
Create a Supabase Edge Function called `hello-world`.

The function should return a JSON response: { "message": "Hello, World!" }

Include proper CORS headers so the function can be called from a browser.

After creating the function, deploy it using the Supabase CLI and show me the 
curl command to test it, using my project's deployed function URL.
```

---

#### Adding Two Numbers Function

```
Create a Supabase Edge Function called `add-numbers`.

The function should read two query parameters, `a` and `b`, add them together 
as numbers, and return a JSON response in the shape: { "result": <sum> }

Requirements:
- Include CORS headers
- Handle the case where `a` or `b` are missing or not valid numbers — return a 
  400 status with a JSON error message explaining what went wrong
- Deploy the function when complete and give me curl commands that test both the 
  happy path and each error case
```

---

##### Handling Parameters

Edge Functions can receive input in two ways. Make sure Claude Code knows which one you want:

**Query parameters** (via the URL — good for simple GET requests):
```
https://your-project.supabase.co/functions/v1/add-numbers?a=5&b=3
```

**Request body** (via POST — good for larger or structured data):
```
POST https://your-project.supabase.co/functions/v1/add-numbers
Content-Type: application/json

{ "a": 5, "b": 3 }
```

When prompting Claude Code, be explicit — tell it which method you want. If you don't specify, ask it to support both and handle each case.

---

## Conclusion

Serverless functions are the escape hatch from your database's limitations. Whenever your application needs to reach outside its own data — to call an API, protect a secret, or run logic the database can't express — an Edge Function is your tool.

As an AI Builder, you won't write these from scratch, but you need to understand *what problem they solve* so you can recognize when to ask Claude Code to create one. The pattern is always the same: receive a request, do something the frontend can't safely do, return a response.

From here, the logical next step is using Edge Functions to protect real secrets — like calling OpenAI from your backend instead of your browser.