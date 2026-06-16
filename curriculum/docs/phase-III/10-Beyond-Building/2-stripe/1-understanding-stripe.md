# Understanding Stripe

## **<a href="https://docs.google.com/presentation/d/1RtcnTAX1NZqoieTstShMH162DhtXn-S1PAANxecBZXo/edit?usp=drive_link" target="_">LECTURE SLIDE DECK</a>

## Intro

At some point, your application will need to collect money. Whether you're building a SaaS product, a marketplace, or a subscription service, payments are one of the most sensitive and regulated parts of any application. You do not want to build this yourself.

Stripe is the industry standard for handling payments on the web. In this lecture, you will not write a single line of Stripe code — instead, you will build a mental model for *how* Stripe fits into a full-stack application, what happens at each step of a transaction, and why it works the way it does. That conceptual foundation is what will allow you to have a productive conversation with Claude Code when it's time to implement.

**By the end of this lecture, you should be able to:**

- Explain what Stripe is and why developers use it
- Describe the cause-and-effect chain of a payment transaction
- Identify what happens on the client side vs. the server side
- Understand what changes when your app is deployed vs. running locally
- Know what to watch out for before going live

---

## Lesson

### What is Stripe?

Stripe is a **payment processing platform**. It is the company that sits between your application and the global banking system, handling the complexity of moving money so you don't have to.

Think of it this way: when a user clicks "Buy" in your app, their credit card information needs to travel through an elaborate financial network — banks, card networks like Visa and Mastercard, fraud detection systems, currency exchanges. Each of those systems has its own protocols, security requirements, and regulations. Stripe handles all of that on your behalf.

From your application's perspective, Stripe is a **service you talk to via an API**. You send Stripe information about what you want to charge, Stripe does the financial heavy lifting, and Stripe tells you whether it worked.

**A critical mental model shift:** Your app never actually processes a payment. Stripe does. Your app's job is to ask Stripe to process a payment, and then respond to what Stripe reports back.

---

### Benefits of Stripe

**1. You never touch raw card data.**
Handling credit card numbers directly would require your application to comply with a security standard called PCI-DSS — an expensive, complex certification. Stripe's architecture is designed so that sensitive card details go directly from the user's browser to Stripe's servers, bypassing yours entirely. This is by design, not coincidence.

**2. Fraud protection is built in.**
Stripe runs its own machine learning models across millions of transactions to detect fraud. This is something no individual developer team could realistically build or maintain.

**3. Global coverage out of the box.**
Stripe handles dozens of currencies, local payment methods (like iDEAL in Europe or Konbini in Japan), and regulatory requirements across countries. Without Stripe, supporting a global product would require separate integrations with regional payment providers in each market.

**4. A developer-first API.**
Stripe has some of the best-documented APIs in the industry. It offers testing tools, sandbox environments, and a dashboard that shows you exactly what's happening with every transaction — all of which make your job as a builder much easier.

**5. Compliance and legal protection.**
Stripe is a licensed financial institution in multiple jurisdictions. When you use Stripe, you're operating under their licenses, which covers a significant portion of the legal and regulatory burden you'd otherwise bear yourself.

---

### How Does Stripe Work With Server Side Logic

The server side — in your stack, this means **Supabase Edge Functions** — is where trust lives. The rule is simple: anything that involves your Stripe secret key must happen on the server, never in the browser.

**Why?** Your Stripe secret key can do almost anything to your Stripe account: issue refunds, create charges, read customer data. If that key ends up in your client-side code, anyone can extract it from your app and make requests on your behalf. The server is the only place where that key is safe.

Here is the order of operations for a typical payment, from the server's perspective:

```
1. The client sends a payment request to your Edge Function
   (e.g., "this user wants to buy the Pro plan")

2. The Edge Function receives the request and validates it
   (Is the user logged in? Is the item they're purchasing real?)

3. The Edge Function uses the Stripe secret key to create a 
   Payment Intent on Stripe's servers
   (a Payment Intent is Stripe's way of representing a pending charge)

4. Stripe returns a client_secret — a short-lived token that 
   represents this specific pending payment

5. The Edge Function sends that client_secret back to the client
```

The server is also where **webhooks** are received. A webhook is a message Stripe sends *to your server* after something happens — a payment succeeds, a subscription renews, a charge fails. This is how your application learns about the outcome of transactions. Your Edge Function needs to listen for these messages and update your database accordingly (e.g., marking a user's account as "paid").

**Key cause and effect:** No action your client takes directly changes payment state in your database. The client triggers a payment → Stripe processes it → Stripe notifies your server via webhook → your server updates your database. The webhook is the source of truth, not the client.

---

### How Does Stripe Work With Client Side Logic

The client side — your **React + Vite** frontend — has a much more limited role in the payment process, and that's intentional.

The client's job is to:

1. Collect the user's payment details *without ever reading them*
2. Send those details directly to Stripe (not to your server)
3. Communicate the user's intent to pay to your server
4. React to the outcome Stripe reports

**How does the client collect card details without reading them?**

Stripe provides a JavaScript library called **Stripe.js**, and within it, pre-built UI components called **Stripe Elements**. When you embed a Stripe Element in your React app, you're embedding an `<iframe>` that Stripe hosts. The card number input your user sees is actually running inside Stripe's infrastructure, not yours. Your React code cannot read what the user types into it — only Stripe can.

Here is the client-side order of operations:

```
1. User navigates to the checkout page in your React app

2. React loads the Stripe Elements component (the hosted card form)

3. User enters card details into the Stripe-hosted form

4. User clicks "Pay"

5. React calls your Edge Function to request a Payment Intent
   (your server creates the intent and returns a client_secret)

6. React passes the client_secret to Stripe.js

7. Stripe.js uses the client_secret + the card details to 
   confirm the Payment Intent directly with Stripe's servers

8. Stripe responds: success or failure

9. React shows the user the appropriate result
   (a success screen, an error message, etc.)
```

Notice that in step 7, the sensitive card data never touches your server. It goes from the Stripe-hosted input directly to Stripe. Your React code only handles the `client_secret` — a token that is useless without the card details it corresponds to.

**Axios's role here:** Axios is used for step 5 — making the HTTP request from your React component to your Edge Function. It is not involved in the actual Stripe payment confirmation, which uses Stripe's own SDK.

---

### How Does Stripe Work Once Deployed

When you are developing locally, Stripe provides a **test mode** — a complete parallel version of their payment system where no real money moves. Test mode uses fake card numbers (like `4242 4242 4242 4242`) and gives you a sandbox to verify your integration without financial risk.

When you deploy to production, several things must change:

**API Keys switch from test to live.**
Stripe gives you two sets of keys: test keys (prefixed with `sk_test_` and `pk_test_`) and live keys (`sk_live_` and `pk_live_`). In production, your Edge Functions and your React app must use the live keys. These are stored as environment variables in your deployment environment — never hardcoded in your source code.

**Webhooks must point to your deployed URL.**
During development, you typically use the Stripe CLI to forward webhook events to `localhost`. Once deployed, you configure Stripe's dashboard to send webhook events to your actual Edge Function endpoint (e.g., `https://your-project.supabase.co/functions/v1/stripe-webhook`). If this is misconfigured, Stripe will process payments but your database will never be updated — users will be charged but never see their access granted.

**HTTPS is required.**
Stripe will not process live payments over HTTP. Your deployed application must be served over HTTPS. Hosting platforms like Vercel, Netlify, and Supabase handle this automatically, but it's worth verifying before go-live.

**Deployment checklist mental model:**

```
Local Dev                    →    Production
─────────────────────────────────────────────────
sk_test_...                  →    sk_live_...
pk_test_...                  →    pk_live_...
Stripe CLI webhook forward   →    Configured webhook URL
localhost:5173               →    your-domain.com (HTTPS)
Fake card numbers            →    Real card numbers
No real money moves          →    Real money moves
```

---

### Things to Note

**Stripe has two main pricing models you'll use: one-time payments and subscriptions.**
A one-time payment is a single charge. A subscription is a recurring charge managed entirely by Stripe — Stripe handles renewal billing, failed payment retries, and cancellation logic. The implementation differs between the two, so know which you're building before you prompt Claude Code.

**The Payment Intent is the center of gravity.**
Almost everything in Stripe's modern API revolves around the Payment Intent object. It represents a single attempt to collect payment. It has a lifecycle: `created → processing → succeeded` or `requires_action` (for things like 3D Secure authentication). When something goes wrong, the Payment Intent's status and last error tell you why.

**Webhooks can arrive out of order or more than once.**
Stripe guarantees delivery but not exactly-once delivery. Your webhook handler should be **idempotent** — meaning it can safely receive the same event multiple times without creating duplicate records. For example, don't just insert a row when you receive `payment_intent.succeeded`; check if that payment has already been recorded first.

**3D Secure (3DS) is a step you can't skip globally.**
In Europe and some other regions, card issuers require an additional authentication step before completing a payment. Stripe handles this flow, but your client needs to be built to handle a `requires_action` state from the Payment Intent, which will redirect the user to their bank's authentication page before the payment completes.

**Test your failure cases, not just your success cases.**
Stripe provides test card numbers that simulate declines, insufficient funds, expired cards, and 3DS challenges. Before launch, make sure your app handles each of these gracefully. A user who gets a cryptic error during a failed payment is a lost customer.

**Never log the full Stripe secret key or card data anywhere.**
Not in your Edge Function logs. Not in Supabase. Not in a debugging console.log you forgot to remove. Treat your `sk_live_` key like a password to your bank account.

---

### Creating Your Stripe Account

To use Stripe in your application, you'll need to create an account at [stripe.com](https://stripe.com). The account setup process will ask for business information — even if you're an individual developer, Stripe treats every account as a business entity for regulatory purposes.

**Key things to do after creating your account:**

1. **Stay in test mode while building.** The toggle between test and live mode is visible in the top-left of the Stripe dashboard. Never use live keys during development.

2. **Find your API keys.** Navigate to *Developers → API keys*. You'll see a publishable key (safe to use in client-side code) and a secret key (server-only). Copy these into your environment variables.

3. **Explore the Stripe dashboard.** The dashboard shows every Payment Intent, customer, subscription, and webhook event in real time. During development, this is your primary debugging tool — if something isn't working, the dashboard will almost always tell you why.

4. **Install the Stripe CLI (optional but recommended).** The Stripe CLI lets you listen to webhook events locally during development, which is essential for testing the full payment flow without deploying.

5. **Enable webhooks before testing end-to-end.** In *Developers → Webhooks*, add an endpoint pointing to your Edge Function and select the events you want to listen to (at minimum: `payment_intent.succeeded`, `payment_intent.payment_failed`).

---

## Conclusion

Stripe is not magic — it is a well-designed system with a clear division of responsibilities. Your client collects intent and renders UI. Your server holds credentials and communicates with Stripe. Stripe handles the financial system, fraud detection, and notifies your server of outcomes. Your server then updates your database to reflect reality.

The most important principle to carry forward: **your database should only reflect what Stripe confirms via webhook, not what your client reports.** Clients can lie, crash, or lose connection. Stripe's webhooks are the authoritative record of what happened financially.

When you sit down with Claude Code to implement Stripe, you now have the vocabulary to direct it precisely: Payment Intent, client_secret, publishable key vs. secret key, Stripe Elements, webhook endpoint, idempotency. That vocabulary is what turns a vague "add payments" prompt into a precise, verifiable implementation.

In the next phase, you'll work with Claude Code to scaffold this integration into your task manager application — one Edge Function and one React component at a time.