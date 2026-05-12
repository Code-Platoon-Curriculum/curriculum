# MCP Servers

![claude](./resources/claude-mcp.png)

## Introduction

The last lecture showed you how to control what Claude *knows* through context management — `CLAUDE.md`, `@`-references, planning mode, and session commands. Claude can now read your project accurately and work within its conventions.

But Claude Code's reach, by default, is limited to what it can do with text: reading files, writing files, running shell commands you approve. It cannot open a browser. It cannot inspect a running site. It cannot interact with a live interface unless you describe its output in text yourself.

**MCP servers** remove that limitation. MCP (Model Context Protocol) is the system that gives Claude direct access to external tools — tools that run real code, interact with real interfaces, and return real results into Claude's context. In this lecture you will learn what MCP servers are, how to install and configure them, and how to use the Playwright MCP server to give Claude the ability to open DevLog in a browser and verify that it actually looks and works the way you intended.

---

## Lesson

### What Is MCP?

**MCP (Model Context Protocol)** is an open protocol that defines how external tools communicate with Claude Code. Think of it as a plugin system: an MCP server is a small program that exposes a set of capabilities — tools, in MCP terminology — that Claude can call during a session.

Without MCP, if you ask Claude to "check that the navigation links work," Claude can only reason about your files. It cannot run the site, open a browser, and click through the menu. With Playwright MCP installed, Claude can do exactly that — open a real browser, navigate, interact, and report back.

MCP servers can expose capabilities in three forms:

| Form | What It Gives Claude | Example |
|------|---------------------|---------|
| **Tools** | Functions Claude can call | `browser_navigate`, `browser_click`, `browser_screenshot` |
| **Resources** | External data Claude can read | Files, database records, API responses |
| **Prompts** | Pre-written prompt templates | Reusable instructions for common tasks |

Most MCP servers you will encounter in practice expose tools — functions that do things and return structured results.

---

### How MCP Servers Work

The flow when Claude uses an MCP tool:

```
Claude decides it needs a tool (e.g., "navigate to /projects")
                    ↓
Claude Code sends the tool call to the MCP server process
                    ↓
The MCP server executes the action (opens a browser, navigates)
                    ↓
The server returns a result (page title, screenshot, visible text)
                    ↓
Claude reads the result and continues its response
```

MCP servers run as separate processes on your machine. Claude Code starts them when a session begins and communicates with them over standard input/output using a structured JSON protocol. From Claude's perspective, an MCP tool call looks the same as any other tool call — the difference is that the MCP server, not Claude Code itself, executes the underlying action.

---

### Installing MCP Servers

Claude Code provides a `/mcp` command for managing MCP servers:

```
/mcp                          → list installed servers and their status
/mcp add <server-name>        → install a server from the registry
/mcp remove <server-name>     → uninstall a server
```

MCP servers can also be configured manually in your Claude Code settings file. For project-level MCP servers — tools that every contributor to DevLog should have — configure them in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

For personal MCP servers — tools you want globally across all projects — configure them in `~/.claude/settings.json`.

> **Restart Claude Code after adding an MCP server.** The server processes are started at session initialization. A running session does not pick up new servers automatically.

---

### Playwright MCP: A Browser for Claude

**Playwright** is a browser automation framework — it can open real browsers (Chromium, Firefox, WebKit), navigate to pages, click links, fill forms, take screenshots, and read page content. The **Playwright MCP server** wraps these capabilities as MCP tools and makes them available to Claude.

With Playwright MCP, Claude becomes a live site reviewer. Instead of asking Claude to reason about whether a page would look right, you ask it to actually open the page and report what it sees.

#### Installing Playwright MCP

In Claude Code:

```
/mcp add playwright
```

Or add it manually to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

Playwright MCP requires Node.js. The first time it runs, it downloads browser binaries automatically.

#### What Tools Playwright MCP Provides

Once installed, Playwright MCP exposes tools that Claude can use directly:

| Tool | What It Does |
|------|-------------|
| `browser_navigate` | Navigates to a URL |
| `browser_click` | Clicks an element by text or CSS selector |
| `browser_type` | Types text into an input field |
| `browser_screenshot` | Takes a screenshot and returns it as an image |
| `browser_get_text` | Returns the visible text of a page or element |
| `browser_wait_for` | Waits for an element to appear before continuing |

Claude selects and sequences these tools based on what you ask it to do — you describe the task in natural language, and Claude figures out which tool calls achieve it.

---

### Using Playwright MCP with DevLog

#### Verifying the Site Loads

The simplest use: confirm that the site renders without errors.

```
Use Playwright to open http://localhost:8000 and take a screenshot. 
Confirm the page loaded and report what you see.
```

Claude will navigate to the URL, take a screenshot, and describe what it found — including any broken layouts, missing styles, or error messages.

#### Checking Navigation Links

More useful: verifying that the nav menu actually works.

```
Use Playwright to open http://localhost:8000. Click the "Projects" 
link in the navigation and confirm that the Projects index page loads. 
Take a screenshot of the result.
```

Claude will click through the nav just as a reader would and report whether the destination page appeared — catching broken links and misconfigured nav entries before a reader does.

#### Verifying a Post Renders Correctly

```
Use Playwright to open http://localhost:8000/posts/2025-01-15-first-week/. 
Confirm the page title is "Week 1 Reflection" and that a "What I learned" 
section is present. Take a screenshot.
```

Claude navigates to the specific post, reads the rendered content, and verifies that the structure matches what was intended — even if the Markdown source looked correct but had a heading-level mistake that broke the layout.

#### Testing Search

```
Use Playwright to open http://localhost:8000. Click the search icon, 
type "git", and take a screenshot after results appear. Confirm that 
at least one result is shown.
```

Claude interacts with the search UI just like a reader would — revealing whether the MkDocs search plugin indexed the content correctly.

---

### When to Use MCP Tools vs. File Inspection

Playwright MCP is powerful, but it does not replace reading and understanding your files. Use the right tool for the task:

| Task | Better Approach |
|------|----------------|
| Checking whether a post has the right frontmatter | `@`-reference the file, ask Claude to inspect it |
| Verifying a navigation link goes to the right page | Playwright MCP — click the link in a real browser |
| Checking `mkdocs.yml` for a missing nav entry | Read the config file with an `@`-reference |
| Confirming a page renders without layout errors | Playwright MCP — see the rendered result |
| Checking that an image path is correct | `@`-reference the file; Playwright if you need to see it rendered |

MCP tools shine for anything that requires a running site — rendered pages, clickable navigation, live search. File inspection shines for anything that can be understood from reading content — structure, frontmatter, configuration.

---

### The MCP Ecosystem

Playwright is one MCP server. The broader MCP ecosystem includes servers for many external systems:

| MCP Server | What It Gives Claude |
|------------|---------------------|
| **Playwright** | Browser automation — navigate, click, screenshot |
| **Filesystem** | Structured file and directory access |
| **GitHub** | Read issues, PRs, and repository data |
| **Fetch** | Make HTTP requests to external APIs |
| **Memory** | Persistent key-value storage across sessions |

For DevLog, the most relevant servers beyond Playwright are **Filesystem MCP** (for structured access to your content directory) and **GitHub MCP** (to let Claude read your repository's issues when planning what to write or fix next).

You can install multiple MCP servers and they coexist — each runs as its own process and exposes its own set of tools. Claude selects which tool to call based on context.

---

### Learn by Doing

**Your task:** With DevLog running locally (`mkdocs serve`), install Playwright MCP and use it to verify three things:

1. The home page loads and the site title is visible.
2. Clicking a navigation link takes you to the correct page.
3. The search bar returns at least one result when you type a keyword from one of your posts.

For each verification, write the prompt you used and the result Claude reported. If Claude finds a failure, describe what was wrong and whether the issue was in the content, the nav config, or the MkDocs configuration.

---

## Conclusion

MCP servers extend what Claude Code can do beyond text. Instead of describing what your site should look like, you can ask Claude to open your site and report what it actually looks like.

- **MCP (Model Context Protocol)** is an open protocol for connecting external tools to Claude Code. MCP servers expose capabilities — tools, resources, and prompts — that Claude can use during a session.
- **Playwright MCP** gives Claude a real browser. You can ask Claude to navigate pages, click links, take screenshots, and verify rendered content against a live running site.
- **Install MCP servers** with `/mcp add <name>` in Claude Code, or by configuring `.claude/settings.json`. Restart Claude Code after adding a server.
- **Use MCP for live behavior** (does this nav link work? does this page render correctly?) and **file inspection for content and config** (is the frontmatter correct? is the nav entry registered?). The two approaches complement each other.

A coding agent that can both read your files and open your site has a complete picture of what you are building. The next lecture will show you how to extend Claude's behavior further — with custom commands that encode domain knowledge, and hooks that enforce project rules automatically.
