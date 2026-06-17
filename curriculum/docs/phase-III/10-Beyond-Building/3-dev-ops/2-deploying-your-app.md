# Deploying your Application

## Intro

You've built something real. A React frontend, a Supabase backend, Stripe donations — all wired together and working locally on your machine. But "working locally" and "live on the internet" are two very different things.

This lecture is about crossing that gap. Deployment is the process of taking code that lives on your laptop and making it accessible to anyone in the world via a URL. For your specific stack — Vite + React on the frontend, Supabase Edge Functions on the backend, and Stripe handling payments — there are three services that need to be configured correctly and aware of each other before a single real user can successfully make a donation or log into their account.

The good news: the tooling has gotten genuinely excellent. What used to require a DevOps engineer and a day of configuration can now happen in about thirty minutes if you understand what you're doing. This lecture makes sure you understand what you're doing.

We'll cover:

- **Vercel** — where your React app lives in production
- **GitHub** — the bridge that connects your code to Vercel (and keeps secrets out of your codebase)
- **Supabase** — already deployed (it's a cloud service), but needs to know your production URL
- **Stripe** — needs a webhook pointed at your live Supabase Edge Function

---

## Lesson

### What is Vercel?

Vercel is a cloud platform built specifically for deploying frontend applications. It's optimized for frameworks like React + Vite, Next.js, and similar — it understands how these projects work and handles the build, hosting, and global delivery automatically.

When you deploy to Vercel, it:

1. Pulls your code from GitHub
2. Runs your build command (`npm run build` → produces `dist/`)
3. Serves the resulting static files from a global CDN (Content Delivery Network) — meaning your app loads fast for users anywhere in the world
4. Gives you a public URL (like `your-app.vercel.app` or a custom domain if you configure one)

Vercel also handles HTTPS automatically. Every deployment gets a valid SSL certificate. You don't configure this — it just happens.

**Why Vercel and not something else?**
There are other options (Netlify, GitHub Pages, Render, AWS). Vercel is the best fit for your stack because it has native Vite support, the free tier is genuinely generous, and its GitHub integration is the smoothest in the industry. It was also built by the same team that created Next.js, so the React ecosystem is first-class.

---

#### How Does Vercel Deploy Your App from GitHub?

This is where the DevOps concepts from the previous lecture become concrete.

When you connect a GitHub repository to Vercel, Vercel installs a **GitHub App** on your repo. This app listens for specific Git events:

- **Push to `main`** → Vercel triggers a production deployment
- **Pull Request opened** → Vercel creates a **preview deployment** — a live, shareable URL for that specific branch, separate from production

Here's what happens under the hood when you push to `main`:

```
git push origin main
  → GitHub receives the push
    → GitHub notifies Vercel (via webhook)
      → Vercel clones your repo at that commit
        → Vercel runs: npm install → npm run build
          → dist/ is deployed to Vercel's CDN
            → your-app.vercel.app is updated
```

This entire process typically takes 30-90 seconds. You can watch it in real time on the Vercel dashboard.

**Preview deployments** are one of Vercel's most powerful features. Every PR you open gets its own URL — something like `your-app-git-feature-auth-yourname.vercel.app`. This means you can share a working version of a feature branch with a teammate (or review it yourself) before it ever touches production. This integrates directly with the branch strategy from the last lecture: `feature/* → dev → main`, with Vercel deploying a preview at each PR stage.

---

#### Creating an Account

1. Go to <a href="https://vercel.com" target="_">vercel.com</a> and click **Sign Up**
2. Choose **Continue with GitHub** — this is important; you want your Vercel account linked to your GitHub account from the start
3. Once logged in, click **Add New Project**
4. Vercel will show you a list of your GitHub repositories. Find your project repo and click **Import**
5. Vercel will auto-detect that it's a Vite project. You'll see it has already filled in:
   - **Framework Preset**: Vite
   - **Root Directory**: `client/` ← **you need to set this manually** since your repo has both `client/` and `supabase/` directories
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Before clicking Deploy, you need to add your environment variables (covered in the GitHub Secrets section below)

---

### GitHub + Git

#### How Does GitHub Help Vercel Deploy?

GitHub does two jobs in your deployment pipeline:

**1. It's the source of truth for your code.**
Vercel doesn't store your code — it always pulls from GitHub. When Vercel deploys, it's deploying whatever is currently on your `main` branch. GitHub is the single authoritative record of what's in production.

**2. It's the event bus that triggers deployments.**
Vercel's GitHub App listens for pushes and pull request events. GitHub fires those events; Vercel reacts to them. Without GitHub, Vercel wouldn't know when to build or what to build.

This is the CI/CD pipeline you learned about in the DevOps lecture, now made concrete with real tools.

---

#### Ensuring `main` is Up To Date

Before you deploy for the first time — and before any significant new deployment — you want to make sure `main` reflects exactly what you intend to ship.

**The standard pre-deployment checklist:**

```bash
# 1. Switch to main and pull the latest
git checkout main
git pull origin main

# 2. Verify the app builds cleanly (no errors)
cd client
npm run build

# 3. If you have a dev branch that's ahead of main, merge it
git checkout main
git merge dev
git push origin main
```

A clean build locally (`npm run build` completes without errors) is your minimum bar before deploying. If it doesn't build locally, it won't build on Vercel either — and you'll see a failed deployment in your dashboard.

**One thing to be careful about:** your `client/.env` file. It contains your `VITE_SUPABASE_URL`, `VITE_SUPABASE_KEY`, and `VITE_STRIPE_PUBLIC_KEY`. This file should be in your `.gitignore` — it should *never* be committed to GitHub. Those values get to Vercel via environment variables, which you configure in the Vercel dashboard — not through your code.

---

#### GitHub Secrets

Here's a concept that trips up a lot of developers: **your app needs secret values to run, but those secret values must never be checked into your Git repository.**

If you commit your Stripe secret key to GitHub, you've leaked it. GitHub repos (even private ones) can be accidentally made public, shared with the wrong person, or accessed via a compromised account. Secrets in code is one of the most common and costly security mistakes in software development.

The solution is **environment variables stored outside your codebase**:

- **For Vercel** (your React frontend): you add environment variables directly in the Vercel dashboard under Project Settings → Environment Variables
- **For Supabase Edge Functions**: you store secrets in the Supabase dashboard under Project Settings → Edge Functions → Secrets, or deploy them via the Supabase CLI
- **GitHub Secrets** (under your repo's Settings → Secrets and variables → Actions): used when you want GitHub Actions CI to have access to secrets during automated workflows — for example, running a test suite that needs a test Supabase URL

**Your project specifically needs three sets of variables:**

**Vercel (frontend):**
```
VITE_SUPABASE_URL=         ← your Supabase project URL
VITE_SUPABASE_KEY=         ← Supabase anon/public key (safe to expose to browser)
VITE_STRIPE_PUBLIC_KEY=    ← Stripe publishable key (safe to expose to browser)
```
Note: The `VITE_` prefix is required by Vite — only variables with this prefix get bundled into the client-side JavaScript. This is intentional: it forces you to consciously decide what's safe to expose.

**Supabase Edge Functions (backend):**
```
STRIPE_SECRET_KEY=                   ← never goes near the frontend
STRIPE_WEBHOOK_SECRET_SNAPSHOT=      ← for verifying Stripe v1 webhook events
STRIPE_WEBHOOK_SECRET_THIN=          ← for verifying Stripe v2 webhook events
```
`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are automatically injected by the Supabase runtime — you do not need to set these manually.

**The rule:** if a variable name does NOT start with `VITE_` in your client code, it should not be in `client/.env` and it should never be in the frontend bundle. If it IS a `VITE_` variable, it's safe to be public-facing — Stripe's publishable key and Supabase's anon key are both designed to be exposed to browsers.

---

### Tying it All Together

Before your app can go fully live, three services need to be correctly configured and aware of each other. Here's the complete picture:

**Service 1: Vercel (your React frontend)**
- Hosts the built `dist/` output from `client/`
- Needs `VITE_SUPABASE_URL`, `VITE_SUPABASE_KEY`, `VITE_STRIPE_PUBLIC_KEY` as environment variables
- Gets a public URL: `https://your-app.vercel.app`

**Service 2: Supabase (your backend)**
- Already live — Supabase is a managed cloud service
- Your Edge Functions (`process-donation`, `stripe-webhook`) are deployed separately via the Supabase CLI
- Needs `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET_SNAPSHOT`, `STRIPE_WEBHOOK_SECRET_THIN` configured as Edge Function secrets
- Has a fixed URL: `https://ampkukwdwqqghnfntvoi.supabase.co`

**Service 3: Stripe (payment processing)**
- Your Stripe dashboard needs a webhook registered pointing to your live Edge Function URL:
  `https://ampkukwdwqqghnfntvoi.supabase.co/functions/v1/stripe-webhook`
- Listening for: `payment_intent.succeeded`, `payment_intent.payment_failed`
- Stripe will give you signing secrets for this webhook — those go into Supabase as `STRIPE_WEBHOOK_SECRET_SNAPSHOT` and `STRIPE_WEBHOOK_SECRET_THIN`

**The dependency chain:**
```
User visits https://your-app.vercel.app
  → React app loads (served by Vercel)
    → User authenticates (Supabase Auth)
      → User clicks donate
        → React calls process-donation Edge Function (Supabase)
          → Edge Function calls Stripe API (using STRIPE_SECRET_KEY)
            → Stripe charges the card
              → Stripe fires webhook to stripe-webhook Edge Function (Supabase)
                → Edge Function verifies + records donation in DB
```

Every arrow in that chain depends on the right secrets being in the right place. One missing variable and the chain breaks.

---

### Deploying your Application

Here's the complete deployment sequence for the first time your app goes live. Follow these steps in order.

**Step 1: Deploy your Supabase Edge Functions**

Your Edge Functions are already written. Deploy them to the remote Supabase project:

```bash
cd supabase

# Deploy the donation processing function
npx supabase functions deploy process-donation --project-ref ampkukwdwqqghnfntvoi

# Deploy the Stripe webhook handler
npx supabase functions deploy stripe-webhook --project-ref ampkukwdwqqghnfntvoi
```

**Step 2: Set Edge Function secrets in Supabase**

In the Supabase dashboard → Project Settings → Edge Functions → Add secret (or via CLI):

```bash
npx supabase secrets set STRIPE_SECRET_KEY=sk_live_... --project-ref ampkukwdwqqghnfntvoi
npx supabase secrets set STRIPE_WEBHOOK_SECRET_SNAPSHOT=whsec_... --project-ref ampkukwdwqqghnfntvoi
npx supabase secrets set STRIPE_WEBHOOK_SECRET_THIN=whsec_... --project-ref ampkukwdwqqghnfntvoi
```

**Step 3: Register your Stripe webhook**

In your Stripe Dashboard → Developers → Webhooks → Add endpoint:
- URL: `https://ampkukwdwqqghnfntvoi.supabase.co/functions/v1/stripe-webhook`
- Events: `payment_intent.succeeded`, `payment_intent.payment_failed`

After creating the webhook, Stripe gives you a **Signing Secret** — copy it into Supabase as the `STRIPE_WEBHOOK_SECRET_SNAPSHOT` (and `_THIN` if you're using the v2 event format).

**Step 4: Deploy to Vercel**

1. Log into [vercel.com](https://vercel.com)
2. New Project → Import your GitHub repo
3. Set **Root Directory** to `client/`
4. Under **Environment Variables**, add:
   - `VITE_SUPABASE_URL` = your Supabase project URL
   - `VITE_SUPABASE_KEY` = your Supabase anon key
   - `VITE_STRIPE_PUBLIC_KEY` = your Stripe publishable key
5. Click **Deploy**

Vercel will run `npm install` and `npm run build` inside `client/`, then serve `dist/`. The whole process takes about 60 seconds.

**Step 5: Test the full flow**

Once deployed, test the complete user journey in production:
1. Visit your Vercel URL
2. Sign up / log in
3. Navigate to `/donate`
4. Use Stripe's test card `4242 4242 4242 4242` (any future expiry, any CVC)
5. Complete the donation
6. Verify in your Supabase dashboard (Table Editor → `donations`) that a row was inserted

If the donation row appears, your entire pipeline is working — Vercel → Supabase Edge Function → Stripe → Stripe Webhook → Supabase DB.

---

### Follow-on Changes

Going live is not a finish line. Your app will change — bugs get fixed, features get added. Here's how to manage those changes safely using the branch strategy from the DevOps lecture.

**The golden rule: never push directly to `main`.**

Every change — no matter how small — should follow this path:

```
feature/* → dev → main
```

**For a small bug fix:**

```bash
# Branch off main (or dev if it's ahead)
git checkout dev
git checkout -b bugfix/fix-donation-amount

# Make your fix
# ... edit files ...

# Commit with a clear message
git add .
git commit -m "fix: correct donation amount calculation in cents"

# Push and open a PR targeting dev
git push origin bugfix/fix-donation-amount
# → open PR on GitHub: bugfix/fix-donation-amount → dev
```

Vercel will auto-create a **preview deployment** for this PR. You get a live URL to test your fix before it merges. Review it, confirm the fix works, then merge.

**For a new feature:**

```bash
git checkout dev
git checkout -b feature/task-due-dates

# Build the feature with Claude Code
# Commit frequently as you go
git commit -m "feat: add due_date column to tasks table"
git commit -m "feat: add date picker to TaskForm"
git commit -m "feat: display due dates in TaskList"

git push origin feature/task-due-dates
# → PR: feature/task-due-dates → dev → review → merge
# → PR: dev → main → Vercel auto-deploys to production
```

**For Edge Function changes:**

If you modify a Supabase Edge Function, the change does not deploy automatically — Vercel only deploys your React frontend. You need to manually re-deploy the Edge Function:

```bash
npx supabase functions deploy process-donation --project-ref ampkukwdwqqghnfntvoi
```

This is an important distinction: your frontend is on autopilot (push to `main` → Vercel deploys), but your backend Edge Functions require a manual deploy step. Consider adding this to your PR checklist if an Edge Function was modified.

**For database schema changes:**

If you change your Supabase database schema (new table, new column, new RLS policy), you apply it via SQL:

```bash
npx supabase db execute --file supabase/migrations/add_due_date.sql
```

Keep your migration SQL files in version control. This gives you a history of every schema change and makes it possible to reproduce your database structure in a new environment.

**Monitoring your live app:**

After every production deployment, check:
- **Vercel dashboard** → Deployments tab: did the build succeed?
- **Supabase dashboard** → Edge Functions → Logs: are the functions running without errors?
- **Stripe dashboard** → Developers → Webhooks → your endpoint: are webhook events being received and acknowledged (200 response)?

If any of those show errors after a deploy, you can roll back immediately on Vercel by clicking **Promote to Production** on a previous deployment.

---

## Conclusion

Deploying a full-stack application with auth, a database, serverless functions, and payment processing used to require a team. Today, with Vercel + Supabase + Stripe + GitHub, a solo developer can ship all of it.

What you've learned today:

- **Vercel** watches your GitHub `main` branch and automatically builds and deploys your React app on every push — no server management required
- **GitHub** is the bridge: it's where your code lives, where your PRs trigger preview deployments, and where secrets are kept *out* of your codebase
- **Environment variables** are how secrets travel safely — `VITE_*` variables go to Vercel, non-`VITE_*` secrets go to Supabase Edge Functions, and nothing sensitive ever touches your Git history
- **Supabase** is already live but needs its Edge Functions deployed separately and its secrets configured before the backend works in production
- **Stripe** needs a webhook registered pointing at your live Edge Function URL — without it, successful payments never get recorded in your database
- **Follow-on changes** follow the same branch strategy: `feature/* → dev → main`, with Vercel preview URLs letting you verify every change before it reaches real users

The deployment you built today has the same architecture used by production applications serving thousands of users. The scale is different; the structure is identical.