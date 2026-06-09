# Supabase

---

## Intro

Welcome back, builders. Last lecture you did the hard thinking work — you read your user stories, extracted your nouns, chose your data types, mapped out your relationships, and drew a visual schema in DrawSQL. You now have a blueprint.

This lecture is about bringing that blueprint to life.

Today you are going to take everything you designed and turn it into a real, live database that your application can read from and write to. You will do this using **Supabase** — a platform built on top of PostgreSQL that gives you a fully managed database, a visual dashboard to inspect and manage your data, and all the infrastructure you need to connect it to a running application.

By the end of this lecture, you will have a Supabase project running, your schema loaded into it, and a connection established from VSCode. Then you will use **Claude Code** to take your DrawSQL diagram and user stories and generate your database schema automatically — and you will know exactly how to supervise and verify the output.

Let's build.

---

## Lesson

### What is Supabase

Supabase is an open-source platform that provides developers with a production-ready backend — built primarily around a **PostgreSQL database** — along with a suite of tools that would otherwise take weeks to build from scratch: authentication, file storage, real-time subscriptions, and auto-generated APIs.

Think of Supabase as a fully furnished apartment. If you were building a backend from scratch, you'd be pouring the concrete foundation, framing the walls, running the electrical, and installing the plumbing yourself. Supabase hands you the keys to a finished apartment — the infrastructure is already there. You just move in and arrange the furniture.

For builders working with agentic tools, Supabase is a natural fit. It exposes your database through a clean, well-documented interface. Claude Code knows how to work with it. And because it's built on PostgreSQL — a standard, widely understood database engine — everything you learned in the last lecture applies directly here.

---

#### What is PostgreSQL

PostgreSQL (often called "Postgres") is one of the most powerful and widely used open-source relational database systems in the world. It has been under active development for over 30 years and is trusted by companies of every size — from solo side projects to systems processing billions of records.

You already know the core concepts: tables, columns, rows, primary keys, foreign keys, relationships. PostgreSQL is the engine that enforces all of those rules and executes your SQL queries.

A few things that make PostgreSQL stand out from other databases:

- **Strong standards compliance.** It follows the SQL standard closely, which means skills transfer directly to other systems.
- **Advanced data types.** It supports `UUID`, `JSONB`, `ARRAY`, and others that simpler databases don't offer natively.
- **Reliability and correctness.** PostgreSQL takes data integrity seriously. If you define a foreign key constraint, it will enforce it — it will never let you insert a `project_id` that doesn't exist in the `projects` table.
- **Extensibility.** Supabase adds extensions on top of PostgreSQL, including `uuid-ossp` (which auto-generates UUIDs for primary keys) and `pgcrypto` (for encryption).

When you write a schema for Supabase, you are writing PostgreSQL. The two are not different things — Supabase is simply a managed platform that runs PostgreSQL underneath and wraps it with tooling.

---

#### Why Supabase?

There are many ways to host a PostgreSQL database. You could run one yourself on a server, use AWS RDS, use Railway, or use PlanetScale. So why Supabase?

**The dashboard.** Supabase gives you a visual table editor that lets you inspect your data, run queries, and manage your schema through a browser. When you're learning and building, being able to *see* your data in a table is invaluable. You can verify that Claude Code created the right tables, that the right rows were inserted, and that relationships are wiring up correctly — all without writing a single SQL query.

**Auto-generated APIs.** The moment you create a table in Supabase, it automatically generates a REST API and a real-time subscription endpoint for that table. Your frontend can start reading and writing data immediately.

**Authentication built-in.** Supabase includes a full authentication system — email/password, magic links, OAuth providers like Google and GitHub — that integrates directly with your database's row-level security. This is weeks of work if you build it yourself.

**The JavaScript client library.** Supabase publishes `@supabase/supabase-js`, a well-maintained npm package that makes it straightforward to connect your React or Node application to your database. Claude Code knows this library well.

**The free tier.** For learning and side projects, Supabase's free tier is generous — two active projects, 500MB of database storage, and 50,000 monthly active users.

For builders who want to move fast, verify their work visually, and hand off well-defined tasks to Claude Code, Supabase is an excellent choice.

---

#### Creating a Supabase Account

Getting started with Supabase takes about two minutes.

1. Navigate to [supabase.com](https://supabase.com) and click **Start your project**.
2. Sign up using your GitHub account (recommended — it's one click) or with an email address.
3. Once logged in, you'll land on your **Supabase Dashboard** — the home for all your projects.

That's it. No credit card required to start. Your account is your workspace; projects live inside it.

---

#### Interacting with the Supabase Dashboard

Before you create your first project, it's worth understanding the major sections of the Supabase Dashboard — because you'll be coming back to these during development.

**Table Editor**
The visual interface for your database tables. You can view all your tables here, browse the rows of data in any table, add rows manually, and edit or delete existing records. Think of this as your visual window into the database — the equivalent of opening a spreadsheet to check your data.

**SQL Editor**
A full SQL query interface built into the browser. You can write and run any SQL statement here — `SELECT`, `INSERT`, `CREATE TABLE`, or anything else. When you need to inspect something specific, debug a query, or run the schema SQL that Claude Code generates for you, this is where you do it.

**Database → Tables**
Distinct from the Table Editor, this section shows you the structural definition of each table — the column names, types, constraints, and relationships. Use this to verify that your schema was created correctly.

**Database → Relationships**
A view of the foreign key relationships across your tables. After Claude Code creates your schema, come here to confirm that the foreign key links between tables are wired up as you designed them in DrawSQL.

**Authentication**
Manage users, configure sign-in providers, and set up row-level security policies. You'll explore this in more depth once your schema is in place.

**Settings → API**
This is where you find the two critical values you'll need to connect your application: your **Project URL** and your **anon/public API key**. You will copy these into your VSCode project's environment variables.

---

#### Creating Your First Project

With your account set up, you're ready to create a project. A project in Supabase is one isolated PostgreSQL database instance with its own URL, API keys, and settings.

1. From the dashboard, click **New Project**.
2. Give your project a **name** — something descriptive, like `workout-tracker` or `task-manager`. This is just a label for your own reference.
3. Set a **database password**. Use something strong — you can generate one or use a password manager. Store this somewhere safe; you'll need it if you ever connect directly via a database client.
4. Choose a **region**. Pick the one geographically closest to you or your expected users. For US-based builders, `us-east-1` or `us-west-1` are both good choices.
5. Select the **Free plan** for now.
6. Click **Create new project**.

Supabase will take about 60–90 seconds to provision your database. You'll see a loading screen — this is Supabase spinning up a real PostgreSQL instance for you. When it finishes, you'll land on your project's home screen.

> **Important:** Before moving on, navigate to **Settings → General** and copy your **Reference ID**. You will need it in the next step to link the Supabase CLI to this project.

---

#### Connecting Supabase to VSCode

Now that your Supabase project is live, you need to establish a connection between your local VSCode environment and your remote Supabase project. You will do this using the **Supabase CLI** — a command-line tool that lets you manage migrations, push schema changes, and interact with your project directly from the terminal, independent of any specific npm project setup.

Open the VSCode terminal with `` Ctrl+` `` (Windows/Linux) or `` Cmd+` `` (Mac).

**Step 1 — Install the Supabase CLI**

Install the CLI as a development dependency:

```bash
npm install supabase --save-dev
```

This installs the CLI locally to the project. You will invoke it using `npx` to ensure you're always running the version pinned to this project.

**Step 2 — Log in to Supabase**

Authenticate the CLI with your Supabase account:

```bash
npx supabase login
```

This will open a browser window asking you to authorize the CLI. Once you approve, your terminal session will be authenticated and the CLI can communicate with your Supabase projects on your behalf.

**Step 3 — Find your Project Reference ID**

Your Project Reference ID is the unique identifier for your Supabase project. To find it, navigate to your project in the Supabase dashboard → **Settings → General**. You'll see a field labeled **Reference ID** — it looks something like `abcdefghijklmnopqrst`. Copy it.

**Step 4 — Link to your remote project**

Back in the VSCode terminal, link your local environment to your remote Supabase project using the reference ID:

```bash
npx supabase link --project-ref <your-project-ref>
```

Replace `<your-project-ref>` with the value you copied. The CLI will prompt you for your database password — this is the password you set when creating the project. After linking, your local environment is connected to your remote project.

**Step 5 — Push schema changes**

Once linked, you can push local schema changes (SQL migration files) directly to your remote database:

```bash
npx supabase db push
```

This is the command you'll use after Claude Code generates or modifies your schema. It takes the SQL migration files in your local `supabase/migrations/` directory and applies them to your live Supabase database. You'll then verify the result in the dashboard — which is exactly what the supervision section of this lecture covers.

> **Note:** At this stage you don't need to push anything yet — your migrations will be generated in the Claude Code step. The goal here is to confirm that the CLI is installed, you're authenticated, and your project is linked. When you run `npx supabase link`, a successful response with no errors is your confirmation.

---

### Leveraging Built Resources

This is where your preparation from the last lecture pays off. You are not coming to Claude Code empty-handed. You have three assets ready:

---

#### User Stories

Your user stories are the highest-level specification of what your application does. They describe *who* uses the app, *what* they want to accomplish, and *why* — and as you learned in the last lecture, the nouns in those stories map directly to your database tables.

When you provide these to Claude Code, they give the agent important context about the *intent* of your schema — not just the structure, but the purpose. An agent that understands that "a user can belong to multiple teams" will make better decisions about foreign keys and junction tables than one that's just looking at a list of column names.

**What to prepare:** Write your user stories in a plain text or markdown file. A clean list is sufficient:

```
- As a user, I want to log workouts so I can track my progress over time.
- As a user, I want to add exercises to a workout so I can record what I did.
- As a user, I want to view my workout history so I can see improvement.
- As a user, I want to set target weights for exercises so I have a goal to hit.
```

Keep them concise and specific. Vague user stories produce vague schemas.

---

#### DrawSQL Graph as a PNG

The visual diagram you built in DrawSQL is more than a reference — it is a specification. When you export it as a PNG and include it in your prompt to Claude Code, you give the agent a visual representation of every table, every column, every relationship, and the direction of every foreign key.

Claude Code can read images. A clear DrawSQL diagram communicates your data model faster and more precisely than paragraphs of description.

**How to export:** In DrawSQL, use the export button (top-right area of the canvas) to download your diagram as a PNG. Name it something clear, like `schema_diagram.png`, and place it in the root of your project or in a `/docs` folder.

**What makes a good diagram for this purpose:**

- Every table is visible and not overlapping.
- Every column has a name and a data type visible.
- Relationship lines are drawn and clearly show which column connects to which.
- The diagram is not zoomed out so far that text is illegible.

If your schema is large and a single screenshot gets crowded, export it in sections — one PNG per logical grouping of related tables.

---

#### DrawSQL SQL Schema

DrawSQL can also export your diagram as a **SQL file** — the actual `CREATE TABLE` statements that define your schema. This is perhaps your most powerful asset. It is the exact PostgreSQL instructions needed to create every table, every column with its correct type and constraints, and every foreign key relationship you designed.

**How to export:** In DrawSQL, look for the **Export SQL** option (typically under the export menu or toolbar). Download the `.sql` file. Open it and read through it — verify that the types match what you chose, that primary keys are present, and that foreign keys reference the correct tables.

A typical exported SQL schema looks like this:

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title VARCHAR(255) NOT NULL,
  is_complete BOOLEAN DEFAULT false,
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

You can take this SQL file directly into Supabase's **SQL Editor** and run it — and your entire schema will be created in seconds. This is an alternative to asking Claude Code to generate the schema, and it's useful as a verification tool: run the exported SQL yourself first, confirm the tables appear correctly in the dashboard, and then use Claude Code for the next layer of work.

---

### Leveraging Claude Code

With your three assets in hand — user stories, DrawSQL PNG, and DrawSQL SQL schema — you are ready to bring Claude Code into the workflow.

Open your terminal and start a Claude Code session in your project directory:

```bash
claude
```

The goal of this session is to have Claude Code load your database schema into Supabase and scaffold the initial data-access layer of your application. Here is how to construct an effective prompt.

**Provide all three assets upfront.**

Don't drip-feed context. Give Claude Code everything it needs at the start of the session:

```
I'm building a task management application for users to be able to create and manage their daily tasks in an easy fashion. I have some resources I would like you to look at and supervise:

Here is my DrawSQL schema diagram:
@<path to diagram>

Here are my user stories:
@<path to stories>

Here is my exported SQL schema that may need some refinements:
@<path to sql>

My Supabase project is already set up within this directory via the suppabase cli with npx.

Please:
1. Review the schema and confirm it matches the provided diagram.
2. Run the SQL schema against my Supabase project to create the tableS **ONE AT A TIME**.
3. After each step, pause and tell me what you did so I can verify it in the dashboard
   before you continue.


Is there any additional information you may need from me?
```

**The pause-and-verify instruction is critical.** Claude Code is capable of executing many steps in rapid succession. For database work — where a mistake means incorrect schema structure that can be tedious to unwind — you want approval gates between steps. Telling Claude Code to pause after each major action gives you the opportunity to open the Supabase dashboard and confirm before the next step runs.

**Ask for one thing at a time if you're unsure.** If you're not yet comfortable reading Claude Code's output and verifying it confidently, break the session into smaller requests:

- First session: just review and load the schema.
- Second session: generate the CRUD functions.
- Third session: connect those functions to your UI components.

This is not inefficiency — it's good engineering practice. Each phase has a clear success criterion you can check before moving on.

**What Claude Code will do:**

Claude Code will read your schema, analyze it against your user stories to catch any mismatches (a table you forgot, a foreign key pointing the wrong direction), and then use the Supabase CLI or the SQL editor to execute the `CREATE TABLE` statements. It will then generate the data-access layer — the JavaScript functions your components will call to fetch, create, update, and delete records.

---

## Conclusion

You now have a complete, working data layer for your application.

You understood what Supabase is and why it's the right tool for this stage of building. You created a project, explored the dashboard, and established a connection from your VSCode environment. You took the assets you built in the last lecture — user stories, a DrawSQL diagram, and an exported SQL schema — and used them as the context package for Claude Code. And you supervised the output, using the Supabase dashboard as your verification tool to confirm that what Claude Code built actually matches what you designed.

This workflow — design first, then build with an agent, then verify — is the foundation of how a competent builder uses agentic tools. The agent doesn't replace your judgment. It accelerates your execution. Your job is to bring the clarity; Claude Code's job is to translate that clarity into running code.

In the next lecture, you will build on this foundation by connecting your data layer to your React components — fetching real data from Supabase and rendering it in your UI. The schema is in place. Now we make it visible.