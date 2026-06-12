# Supabase Authentication

## Intro

You've spent the last lecture understanding *what* authentication is and *how* it works under the hood. You know that Supabase uses a Session + Token Hybrid, that JWTs carry your user's identity, and that Row-Level Security policies enforce who can touch what data.

Now we build it.

This lecture has two parts. First, we restructure your database — backing up what you have, dropping it cleanly, and recreating your tables the right way with authentication baked in from the start. Second, we hand Claude Code two complete prompts that wire up authentication end-to-end in your Supabase project and your Vite + React application.

By the end of this lecture, your task manager will know who its users are.

---

## Lesson

### Simplified Overview of Supabase Auth

Before touching any code, here's the mental model you need to carry through everything that follows.

Supabase Auth maintains a table called `auth.users` in a schema your application code cannot directly write to. Every time someone registers through Supabase Auth, a record is created there automatically. You don't manage it — Supabase does.

Your job is to maintain a **public `users` table** — a mirror of `auth.users` — that lives in your application's public schema alongside your `tasks` table. This is where you store anything your app needs to know about a user beyond what Supabase Auth tracks: display names, preferences, profile data. The two tables stay in sync via a **database trigger**: the moment Supabase creates a record in `auth.users`, the trigger fires and creates a matching record in your public `users` table automatically.

Your `tasks` table then references your public `users` table through a foreign key on `user_id`. Row-Level Security policies sit on top of both tables and use `auth.uid()` — the user's ID pulled directly from their verified JWT — to enforce that users can only see and modify their own data.

Here's the complete picture:

```
User registers / logs in
        │
        ▼
  Supabase Auth
  (auth.users) ──── trigger fires ────► public.users
                                              │
                                              │ user_id (foreign key)
                                              ▼
                                         public.tasks
                                              │
                                        RLS policies
                                     (auth.uid() = user_id)
```

Everything downstream — your React app, your API calls, your data fetching — depends on this structure being correct. That's why we set it up first, before writing a single line of frontend code.

---

### Building Context for Implementing Authentication

#### Supabase Authentication

##### Interacting with the Supabase Dashboard to Back Up and Restart Your Database

Your task manager currently has data in its `users` and `tasks` tables. Before we drop anything, we back it up. This is a habit worth building — never drop tables you can't restore.

**Step 1 — Back up your `users` table**

1. Open your Supabase project and navigate to **Table Editor** in the left sidebar
2. Click on the `users` table
3. In the top-right corner of the table view, click the **Export** button and select **Export to CSV**
4. Save the file somewhere safe — name it something like `users_backup_YYYY-MM-DD.csv`

**Step 2 — Back up your `tasks` table**

1. Repeat the same process for the `tasks` table
2. Save it as `tasks_backup_YYYY-MM-DD.csv`

You now have a local snapshot of all your data. If anything goes wrong during restructuring, you can re-import these CSVs.

Now you are ready to ask claude code to drop your tables and/make changes to your database.

---

#### Single Page Application

Currently our application is not conducting any real authentication method. As far as our client side code knows it's simply just sending a request to confirm the original credentials submitted. 

Now, we want our Front-End application to truly conduct authentication which usually aligns to the following checklist:

- Register: A brand new user can sign up for our application and interact with our site.
- Log In: A returning user can interact with our site and ONLY their corresponding data
- Log out: A logged in user can end their session and exit our website while removing their credentials from the front-end code.
- User Confirmation: While logged in we need to have a way of confirming who the user is
    - while logged in if the user refreshes the browser, we should be able of leveraging the current credentials to recover the logged in `user` and their corresponding`data`

Now we can move forward and start asking Claude Code to adjust our application.

---

### Leveraging Claude Code

You now have everything you need to hand off to Claude Code. The two prompts below are complete — copy them directly into Claude Code, one at a time, starting with the Supabase prompt.

---

#### Supabase Prompt

Within the directory running your supabase project:

```
I have confirmed my application works well with this type of database schema and am now ready to implement authentication methods to my project.

I would like you to take a look at the following resources:

1. User Journey can be found: <path to user journey>
2. The current supabase schema is as follows: <path to current supabase schema>
3. The current testing data I've populated while ensuring this works is here: <path to dir holding the backed up data>

You should know that I've currently deleted all tables existing in my project and it is now an empty project.

Using these resources as context I would like you to conduct the following:

1. alter the user table function as an authentication table
2. ensure proper RLS policies are set where a user can only view the tasks they own.
3. recreate my database tables on supabase

After conducting each action, pause and ask for confirmation that your actions worked correctly before proceeding to the next step.

Do you have any questions before executing this task?
```

---

#### Vite + React Prompt

```
Utilizing the following resources:

- Supabase db schema: <path to db schema>
- user journey: <path to user journey>
- Project API url: <project api url>
- Project API Key: <project public key>

I would like you to update the functionality for the User Authentication process. Consider the following actions a user can take:

- Register: A brand new user can sign up for our application and interact with our site.
- Log In: A returning user can interact with our site and ONLY their corresponding data
- Log out: A logged in user can end their session and exit our website while removing their credentials from the front-end code.
- User Confirmation: While logged in we need to have a way of confirming who the user is
    - while logged in if the user refreshes the browser, we should be able of leveraging the current credentials to recover the logged in `user` and their corresponding`data`

Each of these actions should be an independent phase. Utilize playwright to ensure completion of each phase prior to moving on to the next one.

Do you have any questions before completing these actions?
```

---

## Conclusion

Your task manager is no longer an open house.

Here is what you have now in place:

- A clean database schema where `public.users` mirrors `auth.users` via a trigger, and `tasks` are owned by authenticated users enforced at the database level through RLS
- A complete understanding of each authentication workflow your frontend needs to support — register, login, logout, and protected page loads including refresh
- Two production-ready prompts that hand Claude Code everything it needs to implement authentication end-to-end and verify it with Playwright

The pattern you've followed in this lecture is the same pattern you will use every time you add a significant new capability to an application with agentic tools: understand the concept deeply, restructure your data correctly, map out the workflows, then give Claude Code a precise and phased prompt with verification built in.

Authentication is the gateway to everything that comes next — user-specific data, role-based permissions, and eventually more advanced Supabase features. You now have the foundation.