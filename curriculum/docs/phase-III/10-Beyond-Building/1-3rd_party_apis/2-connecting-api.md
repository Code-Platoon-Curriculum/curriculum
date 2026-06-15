# Connecting an API

## Intro

Your application has a database, it has endpoints, and it has serverless functions capable of reaching the outside world. Now it's time to actually use that capability. In this lecture you'll learn how to evaluate and consume an external API — using the PokéAPI as a concrete example — and wire it into your backend via an Edge Function.

---

## Lesson

### Why External APIs

**"Work Smarter not Harder"**

Every application eventually needs data or functionality it wasn't built to produce itself. Weather data, payment processing, mapping, authentication, AI — building any of these from scratch would take months. External APIs let you stand on the shoulders of teams who already solved those problems.

As an AI Builder, this mindset matters even more. Your job isn't to reinvent wheels — it's to assemble the right tools into something useful. An API is just another tool. When you identify a gap in your project and find an API that fills it, you've just saved yourself an enormous amount of time and complexity.

The question is never *"should I use external APIs?"* It's *"which ones are worth bringing in?"*

---

### How to Choose an API?

Not every API is worth integrating. Before committing to one, run it through this list of questions and see if it's the right fit:

- **Is it well documented?** Can you understand what it does, what it expects, and what it returns within a few minutes of reading? Poor documentation is a red flag.
- **Is it free, or does it fit your budget?** Does it have a free tier that covers your use case, or will costs scale unexpectedly?
- **Does it require authentication?** Some APIs are open, others require an API key or OAuth. Know what you're signing up for before you start building.
- **Is it actively maintained?** Check when it was last updated. A stale API may have breaking bugs and no one fixing them.
- **Is the data reliable and accurate?** An API that returns bad data is worse than no API at all.
- **What are the rate limits?** How many requests can you make per minute or per day? Will that hold up under real usage?
- **Is there a community or support channel?** Forums, GitHub issues, or Discord can be a lifeline when you're stuck.
- **Does it return data in a usable format?** JSON is standard and easy to work with. Anything exotic adds friction.

> There's a huge list of APIs to explore at <a href="https://github.com/public-apis/public-apis" target="_">Public APIs</a> — check it out and see if any of them brings any umph to your project.

---

### The PokéAPI

The <a href="https://pokeapi.co" target="_">PokéAPI</a> is a free, open, well-documented API covering the entire Pokémon universe. It requires no authentication, has generous rate limits, and returns clean JSON — which makes it an ideal first API to learn with. There's no key to manage, no account to create, you can just start making requests.

#### Reading the Documentation

Before writing a single prompt, always read the documentation. The docs tell you everything Claude Code needs to know to use an API correctly — and if *you* don't understand it, you can't verify whether Claude's output is right.

Head to [pokeapi.co/docs/v2](https://pokeapi.co/docs/v2).

##### Understanding What's Available

The docs list every available **endpoint** — the URLs you can call and what resource each one returns. The PokéAPI organizes its endpoints by resource type: Pokémon, Moves, Items, Locations, and more.

For our purposes, the key endpoint is:

```
GET https://pokeapi.co/api/v2/pokemon/{id or name}
```

This returns everything about a single Pokémon — stats, types, abilities, sprites, and more. You can pass either a numeric ID (`/pokemon/25`) or a name (`/pokemon/pikachu`) — both work.

Skimming the endpoint list first tells you what's *possible* before you decide what to build. You might discover a resource you didn't know existed.

##### Understanding Parameters

Parameters are the inputs an endpoint accepts. For this endpoint there's one: the Pokémon's `id` or `name`, embedded directly in the URL path. Some APIs also accept **query parameters** appended to the URL (like `?limit=20`). The PokéAPI uses these on list endpoints to control pagination — for example:

```
GET https://pokeapi.co/api/v2/pokemon?limit=10&offset=20
```

Always check the docs for what parameters are available, which are required, and what format they expect.

##### Understanding the Return

The response from `/pokemon/pikachu` is a large JSON object. The docs show you its full shape. A few key fields to know:

```json
{
  "id": 25,
  "name": "pikachu",
  "types": [
    { "type": { "name": "electric" } }
  ],
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/.../pikachu.png"
  },
  "stats": [
    { "stat": { "name": "speed" }, "base_stat": 90 }
  ]
}
```

The full response contains dozens of fields you won't need. Your Edge Function's job is to **pull out only what your frontend actually uses** and return a clean, trimmed payload. This keeps your responses fast and your frontend code simple.

---

### Integrating the PokéAPI w/ Edge Functions

> Hand this prompt to Claude Code to build the integration:

```
Create a Supabase Edge Function called `get-pokemon`.

The function should:
- Accept a `name` query parameter (e.g. ?name=pikachu)
- Fetch that Pokémon from the PokéAPI at https://pokeapi.co/api/v2/pokemon/{name}
- Return only a trimmed JSON response containing the Pokémon's name and 
  front_default sprite URL in this shape:
  { "name": "pikachu", "sprite": "https://..." }

Requirements:
- Include proper CORS headers so the function can be called from a browser
- Handle the case where the `name` parameter is missing — return a 400 with a 
  descriptive error message
- Handle the case where the PokéAPI returns a non-OK response (Pokémon not found) 
  — return a 404 with a descriptive error message
- Deploy the function when complete and provide curl commands to test the happy 
  path, the missing parameter case, and the not-found case
```

### Integrating the Dog API

The [Dog API](https://thedogapi.com) works similarly to the PokéAPI — it returns dog breed data, images, and more. The difference: it has an **optional API key**. Without one, it still works, but rate limits are tight and certain endpoints are locked. With a free key, those restrictions lift and additional features become available.

This is a pattern you'll encounter constantly in the wild. It's also the moment a new problem appears: **where does the key live, and how do you keep it safe?**

---

#### Secret Keys

An API key is a credential — it identifies *you* to the external service. If someone else gets your key, they can make requests billed to your account, burn through your rate limits, or access data under your identity.

The danger for frontend developers is obvious in hindsight: if you paste an API key directly into your React code, it ships to the browser. Anyone can open DevTools, read the network request, and extract it in seconds. Even if you delete it from your repo later, if it was ever committed to Git, it lives in the commit history.

This is exactly why Edge Functions exist as a middleman. Your React app never touches the key — it calls your Edge Function, and your Edge Function calls the Dog API with the key stored securely on the server side.

---

#### How to Hide Them?

The standard approach is a **`.env` file** — a plain text file that lives at the root of your project and holds your secret values as environment variables:

```
DOG_API_KEY=live_abc123yourrealkeyhere
```

Your code reads the key from the environment at runtime rather than having it written inline:

```typescript
const apiKey = Deno.env.get("DOG_API_KEY");
```

This way the key never appears in your source code. The `.env` file stays on your machine only — but that guarantee only holds if you tell Git to ignore it.

---

#### Prompting Claude Code to Create the Edge Function

> Hand this prompt to Claude Code:

```
Create a Supabase Edge Function called `get-dog-breeds`.

The Dog API base URL is https://api.thedogapi.com/v1. The function should:
- Call the /breeds endpoint on the Dog API to return a list of all dog breeds
- Each breed in the response has an id, name, and temperament field — return 
  only those three fields for each breed in an array
- Attach the API key to every request using the header: x-api-key

The API key must be read from an environment variable called DOG_API_KEY using 
Deno.env.get("DOG_API_KEY") — it must never be hardcoded in the function file.

Requirements:
- Include proper CORS headers so the function can be called from a browser
- Handle the case where the Dog API returns a non-OK response — return a 502 
  with a descriptive error message
- Create a .env file at the root of the project with a placeholder: 
  DOG_API_KEY=your_api_key_here
- Deploy the function when complete and provide a curl command to test it
```

##### Keep Your Secret Key Secret

Before you run anything, open the `.env` file Claude Code created and replace the placeholder with your real key from [thedogapi.com](https://thedogapi.com). Then — before you do anything else — make sure that file never reaches GitHub.

---

#### .gitignore

A `.gitignore` file tells Git which files and folders to never track. Any file listed there will never appear in a commit, never get pushed to GitHub, and never be readable by anyone with access to your repository.

At the root of your project, your `.gitignore` should include:

```
.env
.env.local
.env*.local
```

Adding `.env` here means your secret key stays on your machine only. This is non-negotiable — treat it the same way you'd treat a password.

**One important caveat:** `.gitignore` only protects files that haven't been committed yet. If you accidentally commit a `.env` file first and add it to `.gitignore` afterward, the key is already in your Git history. If that ever happens, treat the key as compromised — go to the Dog API dashboard and rotate it immediately.

**The deployed equivalent — Supabase Secrets**

A `.env` file solves the problem locally, but when you deploy your Edge Function to Supabase, the server doesn't have your `.env` file — it only has the code you pushed. Supabase solves this with **secrets**: environment variables stored securely in your project's cloud environment.

Set a secret via the CLI:

```bash
supabase secrets set DOG_API_KEY=live_abc123yourrealkeyhere
```

Once set, your deployed function can read it the same way it reads the local `.env` value — `Deno.env.get("DOG_API_KEY")` — with no code changes required. The same line works in both environments. Supabase handles the rest.

The full mental model looks like this:

| Environment | Where the Key Lives |
|---|---|
| Local development | `.env` file (gitignored) |
| Deployed to Supabase | Supabase Secrets via CLI |
| Your source code | Never |

---

## Conclusion

External APIs are one of the most powerful tools in your builder's toolkit. Rather than building everything yourself, you can drop in battle-tested services that handle complex problems — and focus your energy on what makes *your* project unique.

The pattern you practiced here applies to every API you'll ever use: read the docs to understand what's available, what parameters it takes, and what it returns — then give that context to Claude Code to wire it into an Edge Function. The API changes, the pattern doesn't.