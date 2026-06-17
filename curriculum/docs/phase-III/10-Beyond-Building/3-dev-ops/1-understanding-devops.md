# DevOps

## **<a href="https://docs.google.com/presentation/d/1N0c6SPL1TSOdoS_Tm44W5HfPuUhrvicRsosLIm7yrTU/edit?usp=drive_link" target="_">LECTURE SLIDE DECK</a>**

## Intro

Welcome to the DevOps module. By this point in the course, you've built real features — React components, Supabase tables, API integrations. Claude Code has been your coding partner, handling the syntax while you focused on what to build and why.

But here's a question worth asking: *once you build something, how do you make sure it keeps working?* How do you ship updates without breaking what's already live? How do teams (or solo developers) manage code across multiple features being worked on at the same time?

That's where DevOps comes in.

This lecture isn't about writing code. It's about understanding the *systems and practices* that surround code — the stuff that determines whether a project stays healthy over time or turns into chaos. Even if you're using AI to write every line, you still need to understand this layer.

---

## Lesson

### What is DevOps?

DevOps is a set of practices, tools, and a cultural philosophy that combines **software development** (Dev) and **IT operations** (Ops) into a unified workflow. The goal is simple: **ship software faster, more reliably, and with fewer headaches**.

Before DevOps existed as a concept, development teams and operations teams worked in silos. Developers would write code and "throw it over the wall" to an operations team who then had to figure out how to deploy and maintain it. This created slow releases, finger-pointing when things broke, and a lot of friction.

DevOps emerged to break down those walls. It brings development and operations together so that the same people (or tightly coordinated teams) are responsible for a feature from the moment it's conceived to the moment it's running in production and being monitored.

For AI Builders like you, DevOps is the layer of discipline that keeps your Supabase backend, your React frontend, and your deployed app from becoming a tangled mess the moment you start working on more than one thing at a time.

---

### How Did DevOps Become a Thing?

DevOps didn't appear overnight. It evolved out of real pain.

In the early 2000s, the dominant model for shipping software was called **Waterfall** — a slow, sequential process where teams would spend months planning, then months coding, then months testing, then finally deploying. A release cycle could take a year. If something was wrong, you wouldn't find out until the very end.

Around 2001, the **Agile Manifesto** pushed back against this. Agile promoted shorter development cycles, collaboration, and responding to change over following a rigid plan. Teams started shipping in smaller pieces, more often.

But Agile mostly focused on the *development* side. Deployments were still painful and risky. In 2009, Patrick Debois and others began formalizing what would become the DevOps movement — influenced heavily by concepts like **lean manufacturing** (reduce waste, improve flow) and **Toyota's production system** (continuous improvement, or *kaizen*).

The rise of cloud infrastructure (AWS launched in 2006, GitHub in 2008) gave DevOps the tooling it needed to actually work at scale. Suddenly, teams could automate deployments, spin up servers programmatically, and version-control their infrastructure.

Today, DevOps is the standard. Companies like Netflix, Amazon, and Google deploy code thousands of times a day. Even small projects benefit from DevOps principles — and your project is no exception.

---

### What All Goes into DevOps?

DevOps is an umbrella term. Under it, you'll find a collection of practices that cover the full lifecycle of software — from writing code to running it in production. Here are the major pillars:

- **Version Control** — Tracking every change to your codebase (you're already doing this with Git and GitHub)
- **Continuous Integration (CI)** — Automatically validating code changes as they come in
- **Continuous Deployment (CD)** — Automatically shipping validated code to production
- **Infrastructure as Code (IaC)** — Managing servers and environments through code, not manual setup
- **Monitoring & Observability** — Knowing what's happening in your app after it ships
- **Security (DevSecOps)** — Baking security practices into the pipeline, not bolting them on at the end

For this course, we'll focus on the three most immediately relevant to your stack: **Version Control**, **CI**, and **CD**.

---

#### Continuous Integration

**Continuous Integration (CI)** is the practice of frequently merging code changes into a shared repository, with each merge automatically triggering a set of checks.

Think of it as an automated quality gate. Every time a developer pushes code or opens a pull request, a CI system wakes up and runs:

- **Automated tests** — Does the new code break anything that was already working?
- **Linting** — Does the code follow the project's style rules?
- **Build checks** — Does the app even compile/build successfully?

If any of those checks fail, the merge is blocked. If they pass, the code is cleared for the next step.

**Why it matters for your stack:**
Your React + Vite frontend has a build step. Your Supabase Edge Functions are TypeScript. A CI pipeline can automatically run `vite build` and `deno check` on every pull request — catching errors before they ever reach production. Services like **GitHub Actions** make this straightforward to set up.

The name "Continuous" is key. The value comes from integrating *frequently* — small changes, often — rather than waiting until a big batch of work is done. Big batches mean big conflicts. Small batches mean small, manageable problems.

---

#### Continuous Deployment

**Continuous Deployment (CD)** takes over where CI leaves off. Once code passes all its checks, CD automatically deploys it to production — no human clicking a "Deploy" button required.

There are actually two related terms worth knowing:

- **Continuous Delivery** — Code is automatically *prepared* for deployment and can be shipped at the push of a button. (Human still presses the button)
- **Continuous Deployment** — Code is automatically *shipped* to production the moment it passes CI. (No button at all)

Most teams land somewhere in between. For example: code merges to `main` → CI runs tests → if tests pass → automatically deploys to staging → a human reviews staging → one click to push to production.

**Why it matters for your stack:**
Your project likely deploys to a platform like **Vercel** or **Netlify** (for the React frontend) and **Supabase** (for the backend). Both of these platforms have built-in CD support — connect your GitHub repo and they'll automatically deploy every push to `main`. That's already a CD pipeline. Understanding what's happening under the hood helps you configure it intentionally rather than accidentally.

---

### Software Development vs DevOps?

These two aren't competing philosophies — but they have different scopes. Understanding the distinction helps you see why DevOps exists.

#### Software Development Life Cycle

The **Software Development Life Cycle (SDLC)** describes the phases a piece of software goes through from idea to delivery:

1. **Planning** — What are we building? Why?
2. **Requirements** — What specifically does it need to do?
3. **Design** — How will we architect it?
4. **Implementation** — Write the code
5. **Testing** — Does it work correctly?
6. **Deployment** — Ship it
7. **Maintenance** — Keep it running, fix bugs, iterate

The SDLC is fundamentally linear in its traditional form (Waterfall), or iterative in Agile. It's focused on *what gets built*.

#### DevOps Life Cycle

The **DevOps Life Cycle** is a continuous loop (often visualized as a figure-eight or infinity loop) with two intersecting cycles:

**Development loop:**
1. Plan
2. Code
3. Build
4. Test

**Operations loop:**
5. Release
6. Deploy
7. Operate
8. Monitor

...and then back to Plan based on what monitoring reveals.

Where the SDLC has a finish line, the DevOps life cycle has no end — it's a continuous loop of improvement. Each monitoring cycle feeds back into planning for the next iteration.

#### "Against" or "Hand in Hand"?

DevOps doesn't replace the SDLC — it *wraps around it*. 

The SDLC answers: *what are we building and how?*
DevOps answers: *how do we build, ship, and operate it sustainably over time?*

You can think of it this way: the SDLC is the recipe, and DevOps is the kitchen. A great recipe means nothing if the kitchen is disorganized, ingredients aren't restocked, and dishes pile up after every meal. DevOps is the set of practices that keep the kitchen running so every recipe can be executed well — repeatedly.

For AI Builders, this means Claude Code helps you execute the SDLC faster (generate code, scaffold features, write tests). DevOps is the structure that ensures what Claude Code produces doesn't break your production environment or create chaos for your teammates.

---

### Version Control (GitHub)

Version control is the foundation that everything else in DevOps sits on. Without it, CI/CD is impossible, collaboration is a nightmare, and rolling back a bad deployment means "hope you remember what the code looked like before."

Git is the version control system. GitHub is the platform that hosts your Git repositories and adds collaboration features on top.

#### The Importance of Version Control in DevOps

Version control does several critical things for a DevOps workflow:

- **History** — Every change is recorded. Who changed what, when, and (with a good commit message) *why*. This is your audit trail.
- **Rollback** — If a deployment breaks production, you can revert to a previous commit. `git revert` is your emergency brake.
- **Collaboration** — Multiple people (or you, working on multiple features) can work on the same codebase simultaneously without overwriting each other's work.
- **Branching** — Branches let you isolate work. A feature doesn't touch production code until it's ready, reviewed, and tested.
- **Automation trigger** — CI/CD pipelines are triggered by Git events. A push to `main`? Deploy. A pull request opened? Run tests. Git events are the heartbeat of the DevOps pipeline.

#### The `main`/`prod` Branch

The `main` branch (sometimes called `master` or `prod`) represents **production-ready code** — the version of your app that is, or could immediately be, running live for real users.

**Rules for `main`:**
- **Nobody commits directly to `main`** — changes only enter through pull requests
- **Every commit on `main` should be deployable** — broken code never lands here
- **`main` is protected** — in GitHub, you can enable branch protection rules to enforce this: require PR reviews, require CI checks to pass before merging, prevent force-pushes

In your stack, a merge to `main` is what triggers your Vercel/Netlify deployment. That's why keeping `main` clean is non-negotiable.

#### The `dev` Branch

The `dev` branch (sometimes called `develop` or `staging`) is the **integration branch** — it's where completed features come together before they're promoted to `main`.

Think of `dev` as a staging environment. Individual features get merged into `dev` first, where they can be tested *together* to make sure they don't conflict. Once everything in `dev` is stable and tested, `dev` gets merged into `main` as a release.

**The flow:**
```
feature/auth → dev → main
feature/stripe → dev → main
```

`dev` often maps to a staging deployment. So `main` → production, `dev` → staging. Your team (or you, reviewing your own work) can preview changes on staging before they go live.

#### Feature Branches

Feature branches are short-lived branches created for a specific piece of work. When you start building something new — a new page, a bug fix, a new Supabase table — you create a branch for it.

**Naming conventions:**
- `feature/user-authentication`
- `feature/stripe-donation-flow`  
- `bugfix/task-not-saving`
- `hotfix/payment-crash`

**The lifecycle of a feature branch:**
1. Branch off from `dev` (or `main` for hotfixes)
2. Build the feature with Claude Code
3. Commit frequently as you go (small, descriptive commits)
4. Push to GitHub and open a Pull Request targeting `dev`
5. CI runs automatically
6. Code gets reviewed (by teammates, or by your future self)
7. Branch gets merged into `dev`
8. Feature branch gets deleted (it's done its job)

In your project, a feature branch for, say, the Stripe donation integration would be `feature/stripe-donation`. Everything related to that integration — Supabase function changes, React component updates, Axios configuration — lives on that branch until it's ready to merge.

#### Bringing it All Together

Here's the complete branching workflow in action, using your actual stack as an example:

**Scenario:** You're adding a new "donation history" page to your app.

1. You're on `dev`. You create `feature/donation-history`
2. Claude Code helps you build the React page, the Supabase query, and the Axios call
3. You commit changes: `git commit -m "feat: add donation history page with Supabase query"`
4. You push and open a PR: `feature/donation-history → dev`
5. GitHub Actions runs your CI: Vite build check + any tests you have
6. CI passes ✅ — PR gets merged into `dev`
7. Staging deployment updates automatically (dev → staging environment)
8. You review the staging URL, everything looks good
9. You open a PR: `dev → main`
10. It merges — Vercel triggers a production deployment
11. 🚀 Live

This workflow protects your production app at every step. Nothing reaches users without passing through CI, review, and staging.

**Visual summary of the branch hierarchy:**

```
main          ←── Only receives merges from dev (or hotfixes)
  ↑
dev           ←── Integration branch; receives feature merges
  ↑
feature/*     ←── Where all active development happens
```

---

## Conclusion

DevOps is not a separate job title or a tool you install — it's a way of thinking about software. It asks: *how do we build things in a way that's sustainable, reliable, and collaborative over time?*

For AI Builders, the SDLC execution layer (writing code, building features) is increasingly handled by tools like Claude Code. That makes the DevOps layer *more* important, not less. Understanding branching strategy, CI/CD pipelines, and deployment workflows is what separates someone who can build a demo from someone who can ship and maintain a real product.

What you've learned today:
- **DevOps** bridges development and operations into a continuous loop
- **CI** automatically validates code on every push — catching errors early
- **CD** automatically ships validated code — removing manual deployment risk
- **SDLC and DevOps** work together: SDLC defines *what* gets built, DevOps defines *how* it gets shipped and operated
- **Git branching** is the practical foundation: `main` is sacred, `dev` is staging, feature branches are where work happens

In your project — with Vite + React, Supabase, and Stripe — you now have a mental model for how changes should flow from your editor to your users: safely, predictably, and with a history you can always roll back to.

Next up: we'll put this into practice by configuring GitHub Actions for your project and wiring it to your deployment pipeline.