# OWASP TOP 10

## **<a href="https://docs.google.com/presentation/d/1ih-23_dnhcIElANkqs9xSL4vInWsgltJ2lAg6aqjukQ/edit?usp=drive_link" target="_">LECTURE SLIDE DECK</a>**

## Intro

You've built something real.

Your application has users, passwords, payment data, and private tasks. It talks to a database, processes transactions, and runs code on a server. That's not a tutorial project — that's a system with real stakes.

Today's lecture isn't about writing security code. It's about developing a mindset — the habit of asking *"who am I trusting here, and should I?"* before a line of code ever gets written.

By the end of this lecture, you'll be able to look at any application — including your own — and identify exactly where it's vulnerable and why.

---

## Lesson

### Why Security Is Important

In 2017, a company called Equifax — one of the three major credit bureaus in the United States — suffered a data breach that exposed the personal information of **147 million people**. Social Security numbers, birth dates, home addresses, driver's license numbers, and credit card data. Nearly half the US population.

The cause? An unpatched vulnerability in a software component they were using. A known fix had been available for months. No one applied it.

The cost: $575 million in FTC settlements, $1.38 billion in total breach-related expenses, and permanent reputational damage to a company trusted with the most sensitive financial data in the country.

This wasn't a sophisticated nation-state attack. It was a missed update.

Security failures don't require genius attackers. They require:

- One unlocked door
- One person who notices it

As builders, you are responsible for locking those doors. Not because you're a security expert — but because you built the house.

**The real cost of a security failure:**

- **Financial** — fines, lawsuits, breach remediation, lost revenue
- **Legal** — GDPR, PCI-DSS, HIPAA violations carry mandatory penalties
- **Reputational** — users leave and don't come back
- **Human** — real people's real data gets exposed or stolen

Security isn't a feature you add at the end. It's a responsibility you carry from the first commit.

---

### Security as a Builder

Here's something most security courses won't tell you directly: **most vulnerabilities aren't caused by bad developers. They're caused by developers who didn't ask the right questions.**

When you use Claude Code to build features, the agent writes functional code. It will implement what you ask for. But "functional" and "secure" are not the same thing. Claude Code will not automatically:

- Enforce who can see whose data
- Validate that user input is safe before processing it
- Protect secrets from being exposed
- Ensure your authentication can't be bypassed

That gap is yours to close. And you close it by asking better questions.

**The security mindset is three questions, asked constantly:**

1. **Who can access this?** — Is this endpoint, page, or piece of data available to the right people and only the right people?
2. **What happens if this input is wrong — or malicious?** — If a user sends unexpected data here, does your system break, leak, or comply?
3. **What am I trusting that I shouldn't be?** — Is there an assumption baked into this code that an attacker could exploit?

These aren't questions for a security audit. They're questions for every feature, every prompt, every pull request.

**Your role as an AI Builder:**

- You set the requirements and the constraints
- Claude Code implements them
- Security requirements are your responsibility to specify
- An unspecified security requirement is an open door

---

### The Trust Boundary Model

Every security vulnerability in existence can be traced back to the same root cause: **a trust boundary that wasn't enforced.**

A trust boundary is the line between two systems, components, or actors where trust is assumed but shouldn't be — or where it's verified when it shouldn't need to be.

Think about your application as a series of layers:

```
[ Browser / User ]
       ↓  ← Trust Boundary 1: Can I trust what the user sends?
[ React Frontend ]
       ↓  ← Trust Boundary 2: Can I trust what the frontend sends?
[ Supabase / Edge Functions ]
       ↓  ← Trust Boundary 3: Can I trust what the API sends?
[ PostgreSQL Database ]
       ↓  ← Trust Boundary 4: Can I trust what the database returns?
[ Third-Party Services: Stripe, etc. ]
```

**The golden rule:** Never trust input from outside your current layer. Always verify before you act.

| Boundary | What Can Go Wrong | Example |
|---|---|---|
| User → Frontend | User sends malicious data | Script injection in a form field |
| Frontend → Backend | Frontend is bypassed entirely | API called directly via Postman |
| Backend → Database | Query is manipulated | SQL injection via unsanitized input |
| Backend → Third Party | Secrets exposed | API key leaked in client-side code |
| Third Party → Backend | Webhook isn't verified | Fake Stripe event triggers free access |

**Key insight:** Your frontend is not security. Anyone can open DevTools, inspect your network requests, and call your API directly — bypassing every client-side check you've built. Security lives in the backend. Always.

**Stack callout — Supabase RLS:**
Row Level Security is Supabase's implementation of a trust boundary between your API layer and your database. Without RLS, your database trusts every authenticated request equally. With RLS, you enforce *at the database level* that users can only read and write their own rows. Your frontend might ask for everything — your database only returns what belongs to the requesting user.

---

### Is Your App Vulnerable?

The honest answer: probably yes, in at least a few ways. Not because you built it badly — but because security is a practice, not a feature.

To understand where your app is vulnerable, you first need a map of known vulnerabilities. The most trusted one in the industry is the OWASP Top 10.

#### What Is OWASP?

OWASP — the **Open Worldwide Application Security Project** — is a nonprofit foundation dedicated to improving software security. It produces free, openly available resources including tools, documentation, and standards used by security teams at companies of every size.

Its most well-known publication is the **OWASP Top 10**: a regularly updated list of the ten most critical web application security risks, ranked by prevalence, exploitability, and impact. It is referenced in compliance frameworks, security audits, and job descriptions across the industry.

Understanding the OWASP Top 10 doesn't make you a security engineer. It makes you a developer who knows what to look for — and what to tell your AI agent to watch out for.

---

#### OWASP Top 10

---

**A01: Broken Access Control**

Broken access control is one of the most prevalent and dangerous vulnerabilities. It arises when unauthorized users exploit weak or improperly implemented access mechanisms. This can occur through URL manipulation, where attackers modify endpoints to access restricted areas, or through misconfigured permissions that allow users to perform actions they shouldn't be able to.

The risks are significant: such exploits can expose sensitive data, compromise other users' accounts, or allow privilege escalation — where a regular user gains admin capabilities.

> **In your app:** Can a logged-in user change the URL or the request to see another user's tasks? If your backend doesn't verify that the task belongs to the requesting user, the answer may be yes. RLS policies in Supabase are your primary defense here.

---

**A02: Cryptographic Failures**

Sensitive data exposures often originate from weak encryption protocols, improper key management, or the complete absence of encryption for critical information. Developers may believe they're safe because they implemented encryption — but did it improperly, such as using outdated algorithms or hardcoding encryption keys directly in source code.

These flaws leave sensitive data like user credentials, payment details, or proprietary information exposed to interception and exploitation.

> **In your app:** Are your Supabase credentials, Stripe secret keys, or other API keys stored in your codebase or exposed in client-side code? A `.env` file that gets committed to GitHub is a cryptographic failure. A secret key that ships to the browser is a cryptographic failure.

---

**A03: Injection (SQL, Command, etc.)**

Attackers target inputs to manipulate queries or commands executed by the system. By crafting malicious input — like `'; DROP TABLE users; --` in a search field — they can cause the application to execute unintended database commands, expose data, or crash entirely.

These vulnerabilities can lead to unauthorized data access, system compromise, or complete application failure.

> **In your app:** Supabase's PostgREST API and parameterized queries provide significant injection protection out of the box. However, any Edge Function that constructs raw SQL strings from user input is a potential injection point. Claude Code will sometimes do this if not explicitly instructed otherwise.

---

**A04: Insecure Design**

Insecure design refers to vulnerabilities rooted in fundamental flaws within an application's architecture — not bugs in the implementation, but wrong decisions made during planning. These weaknesses often arise from neglecting security during the design stage entirely.

Examples include missing input validation layers, insufficient segmentation of sensitive data, or overlooking critical authentication safeguards. Unlike bugs that can be patched, insecure design often requires rebuilding core parts of the application.

> **In your app:** Did you design your data model with the assumption that all authenticated users are trustworthy? Did you consider what happens if a user's JWT token is stolen? These are design questions, and the best time to answer them is before the feature is built — not after.

---

**A05: Security Misconfiguration**

Security misconfiguration arises when systems, frameworks, or libraries are improperly configured, leaving applications vulnerable. Common examples include using default configurations, enabling unnecessary features, mismanaging permissions, or exposing sensitive endpoints like debugging interfaces.

As modern software grows increasingly configurable, the risk of misconfiguration has surged — making it one of the most prevalent vulnerabilities today.

> **In your app:** Is your Supabase project's RLS disabled on any tables? Are your Edge Functions exposed without authentication checks? Did you leave any test endpoints or debug routes active in production? Misconfiguration is one of the easiest vulnerabilities to introduce and one of the easiest to miss.

---

**A06: Vulnerable and Outdated Components**

Libraries and components are application building blocks that speed development by reducing the need to recreate standard functions. But they also carry the risk of harboring unpatched flaws that attackers exploit. These flaws propagate into every application that uses the vulnerable version.

Library issues are particularly tricky because the vulnerability may not be in the library's own code, but in a dependency of a dependency — a vast recursive web that's nearly impossible to audit manually.

> **In your app:** When did you last run `npm audit`? Are you pinning exact versions or using ranges? A dependency with a known vulnerability in your `package.json` is a known open door. Set a habit of checking for updates, especially for auth and payment-related packages.

---

**A07: Identification and Authentication Failures**

Weak authentication mechanisms and poor session management create significant vulnerabilities, opening doors for unauthorized access and session hijacking. Common issues include easily guessable credentials, inadequate password storage practices, insufficient session expiration policies, and flaws in multi-factor authentication.

These weaknesses compromise user accounts and can grant attackers access to sensitive systems, amplifying potential damage far beyond a single user.

> **In your app:** Supabase Auth handles most of this correctly by default — password hashing, JWT expiry, and session management are built in. Your risk here is in how you *extend* it: custom auth flows, long-lived tokens, or bypassing Supabase Auth entirely for certain routes.

---

**A08: Software and Data Integrity Failures**

Software and data integrity failures occur when critical processes — updates, data handling, CI/CD pipeline activities — lack proper validation and verification. Attackers can inject malicious code, tamper with data, or exploit unverified software updates to compromise systems.

Common examples include insecure deserialization (processing untrusted data without validation) and the absence of integrity checks in critical workflows.

> **In your app:** Are you verifying Stripe webhook signatures? A Stripe webhook is an HTTP request from the internet claiming to be from Stripe. Without signature verification, an attacker could send a fake "payment succeeded" event and receive paid features for free. This is a data integrity failure with direct financial consequences.

---

**A09: Security Logging and Monitoring Failures**

Security logging and monitoring failures occur when applications lack adequate mechanisms to capture and analyze critical events, leaving organizations blind to potential breaches or suspicious activity. Without comprehensive logs, security teams struggle to detect, investigate, or respond to incidents — significantly increasing the risk of prolonged and undetected attacks.

Effective logging and monitoring are not just about visibility — they're foundational to timely incident response and long-term security resilience.

> **In your app:** If someone attempted to brute-force your login endpoint right now, would you know? If a user was accessing data they shouldn't, would there be a record? Supabase provides basic logs, but defining what constitutes a suspicious event — and alerting on it — is your responsibility.

---

**A10: Server-Side Request Forgery (SSRF)**

In SSRF attacks, attackers exploit URL handling or insufficient input validation to trick the server into making requests on their behalf — to internal services, cloud metadata endpoints, or other protected resources. These attacks are particularly dangerous because they bypass traditional security measures like firewalls.

This risk increases as organizations rely more on APIs and microservices, which assume internal traffic is trusted.

> **In your app:** If any of your Edge Functions accept a URL as user input and make a request to it, that's a potential SSRF vector. An attacker could supply an internal URL — like a cloud provider's metadata service — and extract credentials or configuration data. Always validate and whitelist URLs before your server fetches them.

---

## Conclusion

You now have a map.

The OWASP Top 10 isn't a list of exotic hacker techniques. It's a catalog of doors that developers — good, professional, experienced developers — left unlocked. Most of them weren't careless. They just didn't ask the right questions at the right time.

You have an advantage they didn't: you know the map before you're out in the field.

The Trust Boundary Model gives you a framework for thinking about every feature you build. Every time you add something to your application, ask: *What new trust boundary does this create? Am I enforcing it?*

And when you're prompting Claude Code, remember: you set the security requirements. If you don't specify them, they don't exist. That's not a limitation of the tool — it's the responsibility of the builder.

In the next lecture, we'll take this off the whiteboard and into a real, intentionally vulnerable application. You'll experience these vulnerabilities firsthand — not as concepts, but as actions with visible consequences. That experience is what turns a map into intuition.

**Key takeaways:**

- Security is a mindset, not a feature — it starts at design time
- Every vulnerability is a trust boundary that wasn't enforced
- The OWASP Top 10 is your industry-standard reference for what to watch for
- AI-generated code is functional by default, not secure by default — your job is to specify the difference
- Next lecture: OWASP Juice Shop — you'll break things before you fix them
