# Handling Context

![claude-code](./resources/claude-code-1.png)

## Introduction

You have learned what Large Language Models are and how to use Claude Code as a general-purpose coding assistant. Now you will apply those skills to a real project with real constraints — DevLog, the personal developer journal you will build throughout this course.

This lecture is about working precisely. A large language model is only as useful as the context it holds. Give it a vague prompt and it makes dozens of guesses — about your project structure, your naming conventions, your content organization, your style rules. Give it the right context and it produces output you can actually use.

In this lecture you will learn four techniques that sharpen Claude's focus: `CLAUDE.md` for persistent project memory, `@`-references for targeting specific files, planning mode for multi-file tasks, and session commands for keeping long sessions accurate and cost-controlled.

---

## Lesson

### The Problem with Generic Prompts

Open a fresh Claude Code session in a new empty folder and type:

```
Build a blog.
```

Claude will build something. It might even look useful. But it will make dozens of decisions without your input — what site generator to use, how to organize posts, what the navigation looks like, what naming conventions to follow — and most of those decisions will not match what you actually want.

Now compare that to:

```
Add a new post to DevLog called "Week 1 Reflection" in docs/posts/.
Follow the post structure described in CLAUDE.md.
```

The second prompt produces a result you can extend. The difference is **context** — Claude knowing what you are building, how you are building it, and what rules apply before it writes a single line.

Every technique in this lecture is about giving Claude that context — and giving it precisely, so that Claude applies it correctly.

---

### CLAUDE.md: Claude's Project Memory

`CLAUDE.md` is a Markdown file that Claude Code reads automatically when you start a session in a project directory. Think of it as the onboarding document you would give a new contributor joining your project: it describes the project, the structure, the conventions, and the rules they need to follow without asking.

Every project you work on with Claude Code should have a `CLAUDE.md`. It is the single most important habit for working efficiently with Claude Code across multiple sessions.

#### Initializing CLAUDE.md with `/init`

Run the following in Claude Code at the root of your project:

```
/init
```

Claude will read your project's existing files and generate a `CLAUDE.md` based on what it finds — structure, configuration, any scripts or conventions it recognizes. Then you customize it.

#### A CLAUDE.md for DevLog

Here is a starting `CLAUDE.md` for DevLog:

```markdown
# DevLog — Developer Learning Journal

## Project Overview
DevLog is a personal documentation site built with MkDocs and the Material 
theme. It serves as a learning journal where entries are written in Markdown 
and organized by topic and date. The site is served locally during writing 
and deployed as a static site via GitHub Pages.

## Tech Stack
- Site generator: MkDocs with Material theme
- Content: Markdown (`.md` files in `docs/`)
- Configuration: `mkdocs.yml`

## File Structure
- `docs/` — all Markdown content files
- `docs/posts/` — individual journal entries, named YYYY-MM-DD-title.md
- `docs/projects/` — project write-ups and retrospectives
- `docs/index.md` — the home page
- `mkdocs.yml` — site navigation, theme, and plugin settings

## Conventions
- Every post must have a top-level `#` heading that matches its nav entry.
- Use frontmatter (`date:`, `tags:`) at the top of every file in `docs/posts/`.
- Never commit the `site/` directory — it is generated output.
- Navigation must be registered in `mkdocs.yml` under `nav:` to appear in the menu.
- Images go in `docs/assets/` and are referenced with relative paths.

## Common Commands
- `mkdocs serve` — live preview at http://localhost:8000
- `mkdocs build --clean` — generate the static site
- `mkdocs gh-deploy` — publish to GitHub Pages
```

Now when you start a Claude Code session in this project, Claude reads this file first and applies all of it to every response — without you repeating yourself.

#### Memory Mode: Updating CLAUDE.md Mid-Session

You can ask Claude to save a fact to `CLAUDE.md` while you are working by prefixing your message with `#`:

```
# All posts in docs/posts/ must include a "What I learned" section 
before the closing heading.
```

Claude will add this instruction to `CLAUDE.md`. Every future session in this project will respect it automatically. Use memory mode when you discover a project-specific rule mid-session that you want to persist.

#### The Three Scopes of CLAUDE.md

`CLAUDE.md` files can live at three levels, and Claude reads all three that apply:

| Location | Scope | Use Case |
|----------|-------|----------|
| `~/.claude/CLAUDE.md` | Global — all projects | Personal habits you always want (output style, communication preferences) |
| `CLAUDE.md` | Project — committed to the repo | Project structure, conventions, content rules. Shared with anyone who contributes. |
| `.claude/CLAUDE.local.md` | Local — not committed | Your personal notes for this project. Machine-specific paths, work-in-progress reminders. |

For DevLog, put the site structure, conventions, and content rules in the project-level `CLAUDE.md`. Put personal notes (like a reminder that your local preview runs on a non-default port) in `.claude/CLAUDE.local.md`.

---

### Scoping Context with @-References

Even with a well-written `CLAUDE.md`, projects have many files. If you ask Claude to "fix the intro post," it will read as many files as it thinks are relevant — sometimes dozens — to build a mental model before answering. This is slow, expensive, and often inaccurate because Claude may read files that are not relevant to your task.

`@`-references solve this by telling Claude exactly which files to look at:

```
Fix the heading structure in @docs/posts/2025-01-15-first-week.md
```

Claude reads specifically that file — not the entire project. The response is faster, cheaper, and more accurate.

Chain references for tasks that touch multiple files:

```
Update the navigation in @mkdocs.yml to include the new post 
added in @docs/posts/2025-01-20-git-basics.md
```

Claude reads both files and produces a change that is consistent with your existing structure — because you told it exactly which files to look at.

#### When to Use @-References

| Situation | What to do |
|-----------|------------|
| Editing a specific post | `@docs/posts/YYYY-MM-DD-title.md` |
| Updating navigation to match a new file | Reference both `mkdocs.yml` and the new file |
| Fixing a formatting issue in a section | Reference the specific file containing that section |
| Starting a new session after `/clear` | Let CLAUDE.md do the work; use `@` to narrow further |

A good rule of thumb: if you know which file the change lives in, reference it. If you are exploring and do not know yet, let Claude scan first, then use `@` to narrow.

---

### Planning Mode for Multi-File Tasks

For a task that touches multiple files — "restructure the DevLog navigation," "add a Projects section with an index page and three entries" — a single-shot prompt often produces incomplete results: some files updated, others missed, navigation not wired up, headings inconsistent.

**Planning mode** (`Shift+Tab` in Claude Code) forces Claude to produce a complete plan before writing anything:

1. Press `Shift+Tab` to enter planning mode.
2. Describe the full task: _"Add a Projects section to DevLog — a projects index page and three project write-up stubs, all registered in the nav."_
3. Claude produces a step-by-step plan: which files to create, which to modify, in what order, and what each change will do.
4. Review the plan. Correct anything that is wrong — a missing file, a wrong path, a step out of order.
5. Approve the plan. Claude executes each step.

Planning mode prevents the "half-done" problem. If Claude does not have a plan, it creates files and discovers missing pieces mid-task — sometimes abandoning consistency to finish. With a plan, you see the full scope first and can redirect before anything is written.

**When to use planning mode:**

| Task size | Approach |
|-----------|----------|
| Single-file edit | Direct prompt with `@`-reference |
| Two or three files | Direct prompt with `@`-references for each |
| Four or more files, or a new section | Planning mode |
| Any task where order of operations matters | Planning mode |

#### Extended Thinking

For deep, single-component reasoning — designing a tagging system, choosing between two navigation structures, deciding how to organize a growing archive of posts — you can ask Claude to think through the problem before answering:

```
Think carefully about the best way to organize posts in DevLog 
so that entries are easy to find by both date and topic.
```

Adding "think carefully" or "think step by step" activates Claude's extended reasoning. The response is slower but more thorough. Reserve it for decisions with significant downstream consequences.

---

### Managing Context Over a Long Session

Claude Code holds the full conversation history in context. Over a long session — many prompts, many file reads, many edits — that history grows large. Old decisions crowd out new ones. Claude starts producing responses that reflect earlier (incorrect) assumptions rather than the current state of the project.

Three commands manage this:

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `/compact` | Compresses conversation history into a summary | The session is long and you want to continue. History is crowding context but you are in the middle of a task. |
| `/clear` | Discards the full conversation and starts fresh | Switching to a completely different task. Or accuracy has drifted and you want a clean slate. CLAUDE.md is still loaded. |
| `/cost` | Shows token usage for the current session | When monitoring what a long session has consumed. |

#### The Pattern for Starting a Session

The most reliable workflow for a DevLog session:

1. Open Claude Code in the DevLog directory — CLAUDE.md loads automatically.
2. Use `@`-references to orient Claude toward the specific file you are working on.
3. For multi-file tasks, press `Shift+Tab` and plan before building.
4. If the session grows long and accuracy drops, run `/compact` to compress.
5. If you are switching to an unrelated task, run `/clear` and start fresh.

The goal is a session where Claude always has the right context and never has so much context that it starts ignoring the relevant parts.

---

## Conclusion

Precise context management is what separates efficient Claude Code use from expensive trial and error.

- **`CLAUDE.md`** is your project's briefing document for Claude. Run `/init` to generate it, then extend it with project-specific rules. Use memory mode (`#`) to update it mid-session. Commit it so anyone who contributes to the project benefits.
- **`@`-references** focus Claude on specific files. If you know where the change lives, reference it. Narrower context produces more accurate results at lower cost.
- **Planning mode** (`Shift+Tab`) is mandatory for any task that touches four or more files. Review the plan before execution so you can catch errors before they are written.
- **Session commands** (`/compact`, `/clear`) keep long sessions accurate. Context that grows unchecked drifts toward inaccuracy. Manage it deliberately.

These four habits compound. A project with a well-maintained `CLAUDE.md`, consistent `@`-referencing, and disciplined session management produces fewer incorrect edits, less rework, and significantly lower token costs than one where Claude is asked to guess at context.
