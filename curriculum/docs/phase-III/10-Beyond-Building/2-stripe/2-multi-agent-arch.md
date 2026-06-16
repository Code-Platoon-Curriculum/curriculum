# Multi-Agent Architecture: Implementing Stripe Donations

## Intro

You already understand *what* Stripe is and *why* it works the way it does. Now we put that knowledge to work.

In this lecture, you will design and deliver a multi-agent Claude Code prompt that implements a one-time donation flow into your existing task manager application. You will not be writing the code yourself — you will be writing the *instructions* that direct Claude Code to write the code for you. That distinction matters. The better your instructions, the better the output.

By the end of this lecture, you will be able to:

- Identify what needs to change on the front end and back end to support a Stripe donation flow
- Design a three-agent Claude Code architecture: one agent per layer, plus a supervisor
- Write a structured multi-agent prompt that Claude Code can execute from start to finish
- Understand what the supervisor agent does and why it exists

---

## Lesson

### Implementing Stripe

Before writing a single prompt, you need a clear picture of what the implementation actually involves. Claude Code cannot plan for you — it can only execute. The planning is your job.

The donation feature has two distinct surfaces that need to work in coordination: the front end that the user interacts with, and the back end that handles money and data. These are different enough in concern that they warrant separate agents.

---

#### Understanding the Front-End Component (Vite + React)

The front end needs to do four things to support a donation:

**1. A Donate UI**
A new page or modal in your existing React app with a donation form. This form will embed a **Stripe Element** — a pre-built, Stripe-hosted card input iframe. The user selects or enters a donation amount and fills in their card details inside that iframe.

**2. An Axios call to your Edge Function**
When the user clicks "Donate," React does not talk to Stripe directly. It calls your own backend via Axios, passing the donation amount. The Edge Function responds with a `client_secret`. This is the only HTTP call Axios makes in this flow.

**3. Stripe.js payment confirmation**
After receiving the `client_secret`, Stripe.js takes over. It packages the card details from the Stripe Element together with the `client_secret` and sends them directly to Stripe to confirm the Payment Intent. React waits for Stripe's response.

**4. Result handling**
React renders a success state (a thank-you message, a confirmation banner, or a redirect) if Stripe confirms the payment, and a descriptive error state if it fails. The user should never see a raw error code.

**What already exists in your project that this connects to:**

- Your existing React Router DOM setup — the donate page is a new route
- Your existing Axios instance — the same one used for task CRUD
- Your existing auth context — the logged-in user's ID should be attached to the donation record

---

#### Understanding the Back-End Component (Supabase)

The back end needs three things:

**1. A new Edge Function: `process-donation`**
This function receives the donation amount from the client, validates that the user is authenticated and the amount is a legitimate value (greater than zero, within reasonable bounds), and then calls the Stripe API using your secret key to create a Payment Intent. It returns the `client_secret` to the client.

**2. A new database table: `donations`**
This table stores the record of every completed donation. It should not be written to by the Edge Function that creates the Payment Intent — it should only be written to by the webhook handler, after Stripe confirms the payment actually went through.

Suggested schema:

| Column | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key, default gen_random_uuid() |
| `user_id` | uuid | Foreign key → auth.users |
| `amount` | integer | In cents (e.g. $10.00 = 1000) |
| `stripe_payment_intent_id` | text | Used for idempotency checks |
| `status` | text | `succeeded`, `failed` |
| `created_at` | timestamptz | Default now() |

**3. A new Edge Function: `stripe-webhook`**
This function listens for Stripe's `payment_intent.succeeded` and `payment_intent.payment_failed` events. When it receives one, it checks whether that `stripe_payment_intent_id` already exists in the `donations` table (idempotency check). If not, it inserts the record. Row Level Security should ensure users can only read their own donation records.

**What already exists in your project that this connects to:**

- Your Supabase auth setup — `user_id` links donations to the authenticated user
- Your existing RLS patterns — the donations table follows the same policy structure as your tasks table
- Your Supabase secrets store — `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` will be added here

---

### Designing a Multi-Agent Prompt

Now that you know what needs to be built, you can design the instructions. A multi-agent Claude Code session uses **sub-agents** — parallel or sequential workers that Claude Code spins up within a single session, each scoped to a specific concern. You are the orchestrator at the human level; the supervisor agent is the orchestrator at the code level.

The architecture for this implementation has three agents:

```
┌─────────────────────────────────────────────┐
│              SUPERVISOR AGENT               │
│  Reviews output of both agents, defines     │
│  passing requirements, decides to proceed   │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────────┐
│  SUPABASE   │  │   UI AGENT      │
│   AGENT     │  │ (React + Vite)  │
│             │  │                 │
│ Edge Fns    │  │ Donate page     │
│ DB schema   │  │ Stripe Elements │
│ RLS         │  │ Axios call      │
│ Webhook     │  │ Result states   │
└─────────────┘  └─────────────────┘
```

The two worker agents run sequentially — Supabase first, UI second — because the UI agent needs to know the Edge Function URL and expected request/response shape before it can write the Axios call. The supervisor runs after both complete.

---

#### Agent 1: Supabase Agent

**Scope:** Everything that lives in Supabase — the database schema, both Edge Functions, RLS policies, and secrets configuration.

**What to include in your prompt for this agent:**

- The name and purpose of the Edge Function it needs to create (`process-donation`)
- The expected request body shape (amount in cents, user ID from auth context)
- The expected response shape (returns `client_secret`)
- The name and schema of the `donations` table (columns listed above)
- The name and purpose of the webhook handler (`stripe-webhook`)
- The two Stripe events to handle (`payment_intent.succeeded`, `payment_intent.payment_failed`)
- The idempotency requirement (check for existing `stripe_payment_intent_id` before inserting)
- The RLS requirement (users can only read their own rows)
- That `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` should be read from Supabase secrets, never hardcoded

**What NOT to include:** Any UI instructions. This agent should have zero awareness of React, components, or routing.

---

#### Agent 2: UI Agent with Playwright

**Scope:** Everything that lives in the React + Vite front end — the new route, the donation form, Stripe Elements integration, the Axios call, and result state rendering.

**What to include in your prompt for this agent:**

- The route path for the donation page (e.g. `/donate`)
- That the card input should use Stripe Elements (not a raw `<input>`)
- The Edge Function endpoint the Axios call should target
- The expected request body (amount in cents) and response shape (client_secret)
- That Stripe.js should be used — not Axios — to confirm the Payment Intent
- The success state UI behavior (what the user sees after a successful donation)
- The error state UI behavior (what the user sees on failure — no raw error codes)
- That the logged-in user's ID should be available from the existing auth context
- **Playwright verification steps** the agent should run after completing the UI:
  - Navigate to `/donate` and confirm the page renders
  - Confirm the Stripe Element iframe is present in the DOM
  - Enter a test donation amount and submit using Stripe's test card `4242 4242 4242 4242`
  - Confirm the success state renders after submission
  - Enter Stripe's decline test card `4000 0000 0000 0002` and confirm the error state renders

**What NOT to include:** Any Supabase or Edge Function implementation details. This agent consumes the API — it does not build it.

---

#### Agent 3: Supervisor and Coordination

**Scope:** Reviewing the output of both agents, defining passing requirements, verifying the integration end-to-end, and deciding whether the implementation is complete or needs correction.

**What to include in your prompt for this agent:**

- That it should review the work of the Supabase agent and UI agent before doing anything else
- That it should **define its own passing requirements** based on what a correct Stripe donation implementation looks like — it should not be handed a checklist. It earns its role by generating the criteria itself.
- That it should verify the following integration points specifically:
  - The UI's Axios call matches the Edge Function's expected request shape
  - The `client_secret` is passed correctly from the Edge Function response to Stripe.js
  - The webhook handler is configured to receive events at the correct URL
  - RLS policies on the `donations` table are correct
  - No Stripe secret key appears anywhere in the front-end code
- That it should run the full Playwright suite after verification
- That if any check fails, it should report specifically what failed and instruct the appropriate agent to correct it — it should not attempt to fix everything itself

**The supervisor's most important job:** It is the only agent explicitly tasked with checking that the secret key never crossed into client-side code. This is a security gate, not a style check.

---

### Leveraging Claude Code

You now have a complete mental model. The final step is putting it into a single, structured prompt that Claude Code can execute.

#### How to Structure the Prompt

Multi-agent prompts in Claude Code work best when they are:

1. **Phased** — each phase has a clear start condition, scope, and completion signal
2. **Scoped per agent** — each agent's instructions are self-contained and do not bleed into the next
3. **Verification-gated** — no phase starts until the previous phase's verification passes
4. **Explicit about the supervisor** — the supervisor's role, authority, and output format are stated clearly

The prompt below follows this structure. Read it fully before submitting it to Claude Code.

---

#### The Prompt

```
You are orchestrating a multi-agent implementation of a Stripe one-time donation feature 
for an existing Vite + React / Supabase task manager application. The application already 
has authentication, RLS policies on existing tables, a Playwright MCP setup, and an Axios 
instance configured for API calls.

Execute the following three phases in order. Do not begin a new phase until the current 
phase's completion criteria are met.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1 — SUPABASE AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spawn a sub-agent scoped exclusively to the Supabase layer. This agent must not touch 
any front-end files.

This agent is responsible for:

1. Creating a new Supabase Edge Function named `process-donation` that:
   - Accepts a POST request with body: { amount: number (in cents), user_id: string }
   - Validates that the user is authenticated and the amount is a positive integer 
     greater than 0 and no greater than 1,000,000 (i.e. $10,000 max)
   - Uses STRIPE_SECRET_KEY from Supabase secrets (never hardcoded) to create a 
     Stripe Payment Intent
   - Returns: { client_secret: string }

2. Creating a `donations` table in the Supabase database with this schema:
   - id: uuid, primary key, default gen_random_uuid()
   - user_id: uuid, foreign key referencing auth.users
   - amount: integer (cents)
   - stripe_payment_intent_id: text, unique
   - status: text ('succeeded' or 'failed')
   - created_at: timestamptz, default now()

3. Creating a Row Level Security policy on `donations` such that:
   - Users can only SELECT their own rows (user_id = auth.uid())
   - No user can INSERT directly — inserts come only from the webhook handler
   - Service role can INSERT and UPDATE

4. Creating a new Supabase Edge Function named `stripe-webhook` that:
   - Listens for POST requests from Stripe
   - Validates the Stripe webhook signature using STRIPE_WEBHOOK_SECRET from 
     Supabase secrets
   - Handles `payment_intent.succeeded`: checks if stripe_payment_intent_id already 
     exists in `donations` (idempotency), and if not, inserts a row with 
     status='succeeded'
   - Handles `payment_intent.payment_failed`: same idempotency check, inserts with 
     status='failed'
   - Returns 200 for all handled events, 400 for signature failures

Phase 1 is complete when:
- Both Edge Functions exist and are deployable without errors
- The `donations` table exists with the correct schema
- RLS policies are in place and correct
- No Stripe secret key appears in any committed file

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2 — UI AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spawn a sub-agent scoped exclusively to the React + Vite front end. This agent must 
not touch any Supabase files, Edge Functions, or database migrations.

This agent is responsible for:

1. Creating a new React page component at the route `/donate` that:
   - Is registered in the existing React Router DOM setup
   - Displays a heading and brief description of the donation feature
   - Includes amount options (suggested: $5, $10, $25, $50) plus a custom amount 
     input
   - Embeds a Stripe Elements card input (CardElement) using @stripe/react-stripe-js
   - Has a "Donate" submit button

2. Implementing the payment flow in the donate page:
   - On submit, use the existing Axios instance to POST to the `process-donation` 
     Edge Function with: { amount: selectedAmountInCents, user_id: currentUser.id }
   - The current user's id is available from the existing auth context
   - On receiving { client_secret }, use Stripe.js (stripe.confirmCardPayment) — 
     NOT Axios — to confirm the Payment Intent directly with Stripe
   - Do not use Axios for the payment confirmation step

3. Rendering clear result states:
   - On success: display a thank-you message that includes the donation amount
   - On failure: display a user-friendly error message (no raw Stripe error codes 
     or stack traces visible to the user)
   - On network error (Edge Function unreachable): display a generic "something went 
     wrong" message and a retry option

4. Running Playwright verification after completing the UI. Use the existing 
   Playwright MCP setup to:
   - Navigate to /donate and confirm the page renders with the expected heading
   - Confirm the Stripe Elements iframe is present in the DOM
   - Select the $10 amount option
   - Complete the card input using Stripe test card: 4242 4242 4242 4242, 
     any future expiry, any CVC
   - Submit and confirm the success state renders
   - Reset and use decline card: 4000 0000 0000 0002
   - Submit and confirm the error state renders with a human-readable message

Phase 2 is complete when:
- The /donate route renders without errors
- The Stripe Elements card input is present and functional
- The Axios call targets the correct Edge Function endpoint
- Stripe.js (not Axios) is used for payment confirmation
- All Playwright verification steps pass

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 3 — SUPERVISOR AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spawn a sub-agent with read access to all files produced by Phase 1 and Phase 2. 
This agent must not write new feature code. It may only correct specific failures 
it identifies and document its findings.

This agent must first define its own passing requirements — before reviewing any 
code — based on what a correct, secure, production-ready Stripe one-time payment 
integration looks like. Document these requirements as a numbered list before 
proceeding.

Then review the output of both agents against those requirements, with explicit 
focus on:

1. API contract alignment: does the UI's Axios call body match exactly what the 
   `process-donation` Edge Function expects? Does it correctly consume 
   { client_secret } from the response?

2. Payment confirmation method: is stripe.confirmCardPayment (Stripe.js) being 
   used for the confirmation step — not a second Axios call?

3. Webhook registration: is the `stripe-webhook` Edge Function URL the one that 
   should be registered in the Stripe dashboard? Document the exact URL.

4. Idempotency: does the webhook handler check for an existing 
   stripe_payment_intent_id before inserting?

5. RLS correctness: can a user read another user's donation rows? Verify the 
   policy logic.

6. Security gate — CRITICAL: scan all front-end files for any occurrence of 
   STRIPE_SECRET_KEY or any string beginning with sk_. If found anywhere in 
   front-end code or committed environment files, this is a hard failure. 
   Report it immediately and halt.

After all checks pass, run the full Playwright suite one final time as an 
end-to-end integration verification.

Phase 3 output must include:
- The supervisor's self-defined passing requirements (numbered list)
- A pass/fail result for each check above
- The webhook URL to register in the Stripe dashboard
- The Playwright suite result (pass or specific failures)
- If any check failed: which agent is responsible and the exact correction needed

Phase 3 is complete when all checks pass and the final Playwright run succeeds.
```

---

#### Before You Submit This Prompt

Work through this checklist in your project before pasting the prompt into Claude Code:

- [ ] Your Stripe account is created and you have your **test** publishable key (`pk_test_...`) and secret key (`sk_test_...`)
- [ ] `STRIPE_SECRET_KEY` has been added to your Supabase project secrets (Settings → Edge Functions → Secrets)
- [ ] `@stripe/stripe-js` and `@stripe/react-stripe-js` are installed in your React project (`npm install @stripe/stripe-js @stripe/react-stripe-js`)
- [ ] Your Playwright MCP is confirmed working (run an existing test to verify before starting)
- [ ] You know the URL of your deployed Supabase project (you will need it to register the webhook URL after Phase 3 reports it)

> **Note on `STRIPE_WEBHOOK_SECRET`:** You will not have this value until after you register your webhook URL in the Stripe dashboard. Add it to Supabase secrets after Phase 3 reports the webhook URL, then trigger a re-deploy of the `stripe-webhook` Edge Function.

---

## Conclusion

What you just designed is not a list of coding tasks — it is a **specification**. Each agent has a defined scope, clear inputs and outputs, explicit completion criteria, and no overlap with the other agents. That structure is what makes the output predictable and verifiable.

The supervisor agent is the part most builders skip. It exists because two agents that each pass their own tests can still fail to work together — the Axios call might use the wrong field name, the confirmation step might use Axios instead of Stripe.js, the secret key might have leaked into an environment file. The supervisor closes those gaps without being told exactly where to look.

The Playwright verification steps are not optional. They are the only way to confirm the integration works as a user experiences it, not just as the code is written. A passing Playwright run on the decline card is as important as a passing run on the success card.

The mental model to carry into every Claude Code session from here: **scope → specify → verify → supervise**. The prompt is the plan. The agents are the execution. The supervisor is the proof.