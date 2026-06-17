# The OWASP Juice Shop

## Intro

In Lecture 1, you built a map. You learned that every vulnerability is a trust boundary that wasn't enforced. You learned the OWASP Top 10 — the industry's catalog of the most critical web application risks. And you learned that AI-generated code is functional by default, not secure by default. Now the map becomes experience.

The OWASP Juice Shop is an intentionally vulnerable web application. Every exploit you've read about exists here — on purpose, waiting to be found. Your job in this lecture is to stop thinking like a builder and start thinking like an attacker. You will break things deliberately, and every time something breaks, you'll feel exactly why it matters.

By the end of this session, you'll have exploited real vulnerabilities firsthand — and you'll never look at your own application the same way again.

---

## Lesson

### What Is the OWASP Juice Shop

The OWASP Juice Shop is a deliberately insecure web application maintained by the Open Worldwide Application Security Project. It is the most widely used security training tool in the world — used by professional penetration testers, security engineers, and developers at companies ranging from startups to Fortune 500s.

It is built to look and feel like a real e-commerce application: it has a product catalog, a shopping cart, user registration and login, an admin panel, and a payment flow. Under the surface, it contains over 100 security vulnerabilities spanning every category in the OWASP Top 10.

**Why it exists:**

Reading about a vulnerability and experiencing one are entirely different things. The Juice Shop exists because the security community recognized that the most effective way to teach a developer not to leave a door unlocked is to show them exactly what happens when someone walks through it.

**What makes it useful for this course:**

Every vulnerability you exploit today maps directly to a concept from Lecture 1. When you bypass login with a SQL injection, that's A03. When you access another user's basket, that's A01. When you download files from an exposed directory, that's A02 and A05 together. The Juice Shop doesn't teach abstract concepts — it makes them visceral.

**One important rule:** Everything you practice here stays here. The skills and techniques in this lecture are for understanding, defense, and authorized testing only. Using them against systems you don't own or have permission to test is illegal under the Computer Fraud and Abuse Act and equivalent laws internationally.

---

### Running Locally w/Docker

The Juice Shop runs inside a Docker container on your machine. Each person runs their own isolated instance — your exploits don't affect anyone else's session, and nothing you do here touches a real server.

**Prerequisites:**

Docker Desktop must be installed and running on your machine. Verify it's active before proceeding — you should see the Docker whale icon in your system tray or menu bar.

You can also open your terminal and run:

```bash
docker ps
```

If you don't get an error, your Docker is good to go.

---

**Step 1 — Pull the Juice Shop image**

Open a terminal and run:

```bash
docker pull bkimminich/juice-shop
```

This downloads the official Juice Shop image from Docker Hub. It is approximately 450MB — run this on a reliable connection.

Expected output:
```
Using default tag: latest
latest: Pulling from bkimminich/juice-shop
...
Status: Downloaded newer image for bkimminich/juice-shop:latest
```

---

**Step 2 — Start the container**

```bash
docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
```

Flag breakdown:

- `-d` — runs the container in the background (detached mode)
- `-p 3000:3000` — maps port 3000 on your machine to port 3000 inside the container
- `--name juice-shop` — gives the container a memorable name for later management

> At this moment you don't need to understand this, we will dive into it within the FS Engineering Program but for now just focus on getting this up and running.

---

**Step 3 — Verify it's running**

```bash
docker ps
```

You should see `juice-shop` listed with a status of `Up`. Then open your browser and navigate to:

```
http://localhost:3000
```

You should see the Juice Shop storefront — a green-themed e-commerce site selling fruit juices. If the page loads, you're ready.

---

**Step 4 — Stopping and restarting**

To stop the container at the end of the session:
```bash
docker stop juice-shop
```

To restart it in a future session:
```bash
docker start juice-shop
```

To wipe your progress and start completely fresh (resets all data):
```bash
docker stop juice-shop
docker rm juice-shop
docker run -d -p 3000:3000 --name juice-shop bkimminich/juice-shop
```

---

**Troubleshooting:**

- **Port already in use:** Another process is using port 3000. Either stop that process or change the port mapping: `-p 3001:3000` and navigate to `http://localhost:3001` instead.
- **Container exits immediately:** Run `docker logs juice-shop` to see the error output.
- **Page won't load:** Wait 15–20 seconds after starting the container — the application takes a moment to initialize before accepting connections.

---

### Exploiting Vulnerabilities

Before we begin: the Juice Shop tracks your progress on a scoreboard that is itself a hidden challenge. Finding it is your first task — and finding it teaches you something important about how information leaks.

---

#### Finding the Scoreboard

**What we're doing and why:**

The scoreboard isn't linked anywhere in the Juice Shop's visible navigation. It exists, but the application assumes you won't find it because it isn't advertised. This is a form of security through obscurity — hiding functionality rather than protecting it. It's a useful first lesson: hiding something is not the same as securing it.

**The concept:** Modern single-page applications load their JavaScript upfront. That JavaScript contains the application's routing logic — including routes for pages that aren't linked in the UI. If you can read the source code, you can discover hidden routes.

---

**Demo Steps:**

1. Navigate to `http://localhost:3000` in your browser.

2. Open DevTools (`F12` or right-click → Inspect).

3. Go to the **Sources** tab (Chrome) or **Debugger** tab (Firefox).

4. In the file tree on the left, locate and open `main.js` — the primary application bundle.

5. Once the file loads, use **Find** (`Ctrl+F` / `Cmd+F`) to search for the string:
   ```
   score-board
   ```

6. You will find a route definition referencing `score-board` in the application's routing configuration. This reveals the path.

7. Navigate to:
   ```
   http://localhost:3000/#/score-board
   ```

8. The scoreboard loads, and your first challenge — "Find the carefully hidden 'Score Board' page" — is marked complete with a green banner.

---

**What just happened:**

You didn't hack anything in the traditional sense. You read publicly available JavaScript that ships to every browser that visits the site. The route existed; it just wasn't linked. The application trusted that users wouldn't look for what they couldn't see — and that trust was misplaced.

> **Lecture 1 Connection — A05: Security Misconfiguration**
> Exposing internal routes, admin panels, or debug endpoints in client-side JavaScript is a misconfiguration. The scoreboard path isn't sensitive — but this exact technique is how attackers discover admin panels, internal APIs, and debug interfaces that were "not linked" but never access-controlled. Security through obscurity is not security.

---

#### Broken Authentication

**What we're doing and why:**

We are going to log in to the Juice Shop as the administrator without knowing the administrator's password. We will do this using a SQL injection on the login form — exploiting the fact that the application constructs its database query by concatenating user input directly into a SQL string rather than using parameterized queries.

This is the most visually dramatic exploit in today's session. When it works, you will see the admin dashboard with full access to every user account in the system.

**Setup:** Make sure you are logged out of the Juice Shop before beginning. If you are logged in, click the account icon and select Logout.

---

**Demo Steps:**

1. Navigate to `http://localhost:3000/#/login`.

2. In the **Email** field, enter exactly:
   ```
   ' OR 1=1 --
   ```
   > Note: there is a space after the two dashes. The space is required for the comment to be valid SQL in some database engines. If it doesn't work, try without the trailing space.

3. In the **Password** field, enter anything — the value does not matter:
   ```
   anything
   ```

4. Click **Log in**.

5. You are now logged in as `admin@juice-sh.op` — the application's administrator account. The Juice Shop confirms this with a green challenge-completion banner: "Log in with the administrator's user account."

---

**What just happened:**

The login query the application ran looked something like this:

```sql
SELECT * FROM Users WHERE email = '' OR 1=1 --' AND password = '...'
```

Breaking this down:
- The single quote `'` closed the email string early
- `OR 1=1` made the condition always true — matching every row in the Users table
- `--` commented out the rest of the query, including the password check entirely

The database returned the first user in the table — which happened to be the admin. The application saw a valid user returned and granted full access.

No password was required. No brute force was needed. The door was open because the application trusted that user input would only ever be an email address — and it was wrong.

> **Lecture 1 Connection — A03: Injection & A07: Identification and Authentication Failures**
> This exploit combines two OWASP categories. The injection vulnerability (A03) allowed the attacker to manipulate the SQL query. The authentication failure (A07) is that the application had no secondary defense — no parameterized queries, no rate limiting, no anomaly detection. Each layer trusted the one before it without verifying. In your own app: Supabase's PostgREST API protects you from this in standard queries, but any Edge Function that concatenates user input into raw SQL is identically vulnerable.

---

#### Broken Access Control

**What we're doing and why:**

We are going to view another user's shopping basket — not our own — by manipulating a number in an API request. No special tools are required. This exploit requires only a browser and the ability to change a single digit.

This demonstrates the most common and most dangerous category on the OWASP Top 10: the application authenticates the user correctly, but never verifies that the resource being requested actually belongs to them.

**Setup:** You will need to be logged in as a regular user for this exploit. First, log out of the admin account. Then either register a new account or log in with:
- Email: `jim@juice-sh.op`
- Password: `ncc-1701`

---

**Demo Steps:**

1. After logging in, click the basket icon in the top navigation to view your basket. The URL will update to reflect the current view.

2. Open DevTools (`F12`) and navigate to the **Network** tab.

3. Refresh the page with DevTools open. Look through the network requests for a call to:
   ```
   /rest/basket/
   ```
   You will see a request like `/rest/basket/6` (the number will vary based on your user's basket ID).

4. Note the basket ID number in that request.

5. In the browser address bar or directly in the Network tab, navigate to:
   ```
   http://localhost:3000/rest/basket/1
   ```
   (Use `1` — this is the administrator's basket ID.)

6. The server returns the full contents of the administrator's basket as a JSON response. You have just read another user's private data.

7. The Juice Shop awards the challenge: "View another user's shopping basket."

---

**What just happened:**

The request to `/rest/basket/6` was authenticated — the application knew who you were. But the request to `/rest/basket/1` was also accepted, because the server checked "are you logged in?" and not "does basket 1 belong to you?"

The basket ID is what security engineers call an **Insecure Direct Object Reference (IDOR)** — a type of broken access control where the identifier for a resource is exposed and predictable, and the server doesn't verify ownership before returning it.

The fix is one check on the server: before returning a basket, verify that the basket's `userId` matches the authenticated user's ID. That check doesn't exist here.

> **Lecture 1 Connection — A01: Broken Access Control**
> This is the textbook IDOR exploit. The trust boundary between the API layer and the database was not enforced — the API trusted that any authenticated user requesting a basket had the right to see it. In your own app: if your Supabase queries fetch tasks by ID without an RLS policy verifying ownership, your application has this exact vulnerability. A logged-in user could request any task by changing a single number.

---

#### Sensitive Data Exposure

**What we're doing and why:**

We are going to access a directory of files on the Juice Shop server that is publicly reachable via URL — no authentication required, no exploit needed. The files are simply sitting there, accessible to anyone who knows or guesses the path.

This exploit requires zero technical skill. It is the most sobering demo of the session because it illustrates that some of the most damaging security failures are also the most mundane.

**Setup:** You can be logged in or logged out — it makes no difference. This endpoint requires no authentication at all.

---

**Demo Steps:**

1. In your browser, navigate directly to:
   ```
   http://localhost:3000/ftp
   ```

2. A directory listing renders in the browser — a list of files hosted on the server with direct download links. Files include:
   - `acquisitions.md` — a document describing planned company acquisitions (sensitive business data)
   - `eastere.gg` — an easter egg file
   - `incident-support.kdbx` — a KeePass password database file
   - `package.json.bak` — a backup of the application's dependency manifest
   - `suspicious_errors.yml` — internal error log configuration
   - Several other internal documents

3. Click `acquisitions.md` to download and open it. Read the contents — it contains fictional but clearly sensitive internal business information.

4. The Juice Shop awards the challenge: "Access a confidential document."

5. Now attempt to access a file with a restricted extension. Navigate to:
   ```
   http://localhost:3000/ftp/eastere.gg
   ```
   The server returns a 403 error for `.gg` files — but not for `.md` or `.pdf` files. This means the restriction is partial: someone configured a block on certain file types but left others fully exposed.

---

**What just happened:**

There was no attack here. No injection, no credential theft, no session manipulation. A directory existed on a public-facing server with no access control. Anyone with the URL could reach it. The files weren't hidden, encrypted, or protected in any way.

The partial restriction on `.gg` files actually makes this worse, not better — it reveals that someone was aware this endpoint existed and attempted a fix, but implemented it incompletely. A partial fix with visible evidence of an attempt is a misconfiguration, not a safeguard.

> **Lecture 1 Connection — A02: Cryptographic Failures & A05: Security Misconfiguration**
> This exploit combines two categories. The sensitive data exposure (A02) is that confidential files were accessible without encryption, authentication, or access control of any kind. The misconfiguration (A05) is that the `/ftp` endpoint was left publicly accessible and the partial file-type restriction created a false sense of security. In your own app: any Supabase Storage bucket set to public, any environment file accidentally committed, or any Edge Function endpoint without an auth check is this exact vulnerability — just with your users' real data.

---

## Conclusion

You've done something today that most developers never do: you've been on the other side.

You found a hidden route by reading JavaScript. You logged in as an administrator without a password. You read another user's private data by changing a single digit. You downloaded confidential files from an unprotected directory. None of these required expertise. None required special tools. They required curiosity and the knowledge of where to look — which you now have.

Take a moment to sit with that before moving on to independent exploration. Every one of these vulnerabilities has a real-world equivalent. The IDOR you exploited is the same class of bug that exposed 114 million accounts in the 2019 Facebook vulnerability. The SQL injection you used is the same technique behind some of the largest data breaches in history. The exposed `/ftp` directory is the same misconfiguration that has leaked internal documents from companies that absolutely should have known better.

The question is no longer "could my app have vulnerabilities?" It's "which ones does it have, and am I asking my AI agent to close them?"
