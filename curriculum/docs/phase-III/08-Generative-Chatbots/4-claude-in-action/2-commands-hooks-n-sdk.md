# Commands, Hooks, and SDK

## Introduction

The last lesson showed you how to control what Claude *knows* — managing context, defining paths, and extending its tools with MCP servers. This lesson shows you how to control what Claude *does* and how it *behaves* within a project.

Three mechanisms give you that control:

- **Commands** — slash-prefixed shortcuts that trigger specific behaviors or run reusable prompt templates you define once per project
- **Hooks** — event-driven scripts that run automatically at defined points in Claude's lifecycle, letting you enforce rules and automate checks without adding prompts
- **SDK** — the Anthropic Python and JavaScript libraries that let you call Claude programmatically from inside a hook, enabling hooks that don't just guard behavior but actively analyze it

By the end of this lesson, the `task_manager` project will have a custom command for security audits, a hook that blocks Claude from reading `.env` files, and a second hook that calls Claude to review every file it edits.

---

## Lesson

### Commands

#### What are Commands?

A **command** is a `/`-prefixed instruction you type into Claude Code that triggers a specific behavior. Some commands are built in to Claude Code and available in every project. Others are custom — project-specific prompts you define once and reuse.

The distinction matters: built-in commands control how Claude Code *operates* (session management, model selection, output style). Custom commands control how Claude *reasons* about your specific project — encoding context and instructions that would otherwise require lengthy prompts every time.

---

#### Built-in Commands

These ship with every Claude Code installation:

| Command | What It Does | When to Use It |
|---------|-------------|----------------|
| `/init` | Scans the project and writes a `CLAUDE.md` with architecture notes | At the start of every new project |
| `/help` | Lists all available commands and key bindings | When you forget what's available |
| `/compact` | Compresses conversation history to reclaim context space | After a long exploration session, before writing code |
| `/clear` | Discards the full conversation context and starts fresh | When switching to an unrelated task |
| `/model` | Switches the active model mid-session | When task complexity changes |
| `/output-style` | Sets verbosity: Default / Explanatory / Learning | When you want more or less explanation |
| `/cost` | Shows token usage for the current session | When monitoring API spend |

For the `task_manager`, the most useful sequence at session start is:

```text
/init          → generates CLAUDE.md with project structure
# <memory>     → add task_manager-specific instructions (email auth, app boundaries)
/output-style  → Learning for development, Default when speed matters
```

---

#### Custom Commands

Custom commands live in `.claude/commands/` at your project root. Each `.md` file becomes a slash command: a file named `security-audit.md` becomes `/security-audit`.

When you invoke the command, its markdown content is sent to Claude as a prompt. You write the instruction once; Claude executes it on every invocation.

```
task_manager/
└── .claude/
    └── commands/
        ├── security-audit.md   → /security-audit
        └── check-api.md        → /check-api
```

> After creating a command file, close and relaunch Claude so it picks up the new command.

**Creating a `security-audit` command for the task_manager:**

The `task_manager` has several known problem areas: a hardcoded `SECRET_KEY`, `DEBUG=True` in production settings, no `max_length` on `Task.title`, and auth tokens stored in `localStorage` instead of `HttpOnly` cookies. A custom command encodes all of that domain knowledge so you never have to re-explain it:

```markdown
<!-- .claude/commands/security-audit.md -->
Perform a focused security audit of the task_manager project. Check each of the following:

1. @server/task_proj/settings.py — Is DEBUG set to True? Is SECRET_KEY hardcoded?
2. @server/task_app/models.py — Does Task.title have a max_length constraint?
3. @server/user_app/views.py and @server/task_app/views.py — Are all endpoints
   protected with IsAuthenticated? Are any missing permission classes?
4. @client/src/utilities.jsx — Is the auth token stored in localStorage?
   What are the XSS implications of this approach?

For each issue found, report: file path, the specific line, severity (low / medium / high),
and a one-sentence fix.
```

Typing `/security-audit` now runs this full analysis without rekeying any of it.

> **Custom commands accept arguments.** Reference them inside the markdown with `$ArgName`. A `/check-endpoint $Route` command could accept `/check-endpoint /api/tasks/` and use that value inside its prompt.

---

● **Learn by Doing**

**Context:** The `security-audit` command above encodes problems we already know about. A project also benefits from commands that assist regular development — not just audits. The task_manager has two separate Django apps (`user_app` and `task_app`), each with their own views and URL configs. Commands that encode this topology save Claude from rediscovering it every session.

**Your Task:** Create `.claude/commands/check-api.md` inside the task_manager project directory. Write a custom `/check-api` command that instructs Claude to verify the API layer. Look for the `TODO(human)` comment in the template below — replace it with the actual verification steps:

```markdown
<!-- .claude/commands/check-api.md -->
<!-- TODO(human): Write a /check-api command for the task_manager.
     The command should instruct Claude to:
     - Identify all API endpoints in both apps (reference correct @paths)
     - Check that each endpoint handles the correct HTTP methods
     - Verify authentication is enforced where expected
     - Report any endpoint that looks incomplete or inconsistent
     Replace this comment with the full command prompt. -->
```

**Guidance:** The goal is a command Claude can execute without already knowing the codebase. Reference source files with `@`-paths so Claude reads them directly rather than guessing. Think about what "incomplete" means for a REST endpoint — a view with no permission class, a URL pattern with no matching serializer field, a `POST` handler with no input validation. The task_manager has at least one of these.

---

### Claude Hooks

#### What are Claude Hooks?

**Hooks** are executables — shell scripts, Python files, Node scripts — that Claude Code runs automatically when specific events occur in the agent loop. They are not prompts; they are code that executes *outside* of Claude's reasoning, enforcing rules or triggering automation that doesn't depend on Claude's judgment.

The pattern: you register a hook type, optionally a matcher (which tool name triggers it), and the command to run. Claude Code passes the tool's full input to your script on `stdin`. Your script reads it, decides what to do, and writes a structured JSON response to `stdout` that Claude Code interprets — either blocking the action, allowing it, or injecting additional context.

This gives you a control layer that sits *below* Claude's reasoning. You can deny a file read before Claude decides whether to use the result. You can inject feedback after a write. You can block an edit without asking Claude for permission.

Hooks can be defined in `.claude/settings.json` (committed, shared with contributors) or `.claude/settings.local.json` (personal, not committed).

---

#### Types of Hooks

| Hook | When It Fires |
|------|--------------|
| **PreToolUse** | Before a tool executes — can deny the call entirely |
| **PostToolUse** | After a tool completes — can inject additional context into Claude's next turn |
| **UserPromptSubmit** | When you submit a prompt, before Claude processes it |
| **Notification** | When Claude needs a permission decision, or after 60 seconds of idle |
| **Stop** | When Claude Code finishes responding |
| **SubagentStop** | When a subagent (displayed as "Task") finishes |
| **PreCompact** | Before a `/compact` operation |
| **SessionStart** | When starting or resuming a session |
| **SessionEnd** | When a session ends |

---

#### Defining Hooks

Hooks are registered in `.claude/settings.json`:

```json
{
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Read",
                "hooks": [
                    {
                        "type": "command",
                        "command": "node ./hooks/read_hook.js"
                    }
                ]
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Write|Edit|MultiEdit",
                "hooks": [
                    {
                        "type": "command",
                        "command": "python3 ./hooks/review_hook.py"
                    }
                ]
            }
        ]
    }
}
```

The `matcher` field is a regex pattern that filters by tool name. `"Read"` fires only on file reads. `"Write|Edit|MultiEdit"` fires on any file modification. Omit the matcher entirely to catch all tool calls for that hook type.

---

### Writing a PreToolUse Hook for `.env`

The `task_manager` ships with a `.env` file containing database credentials and a Django secret key. Claude has no reason to read this file — everything it needs is in the source code. A `PreToolUse` hook on the `Read` tool denies access before the read happens.

#### JavaScript

```javascript
async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());

  const readPath =
    toolArgs.tool_input?.file_path || toolArgs.tool_input?.path || "";

  if (readPath.includes('.env')) {
    process.stdout.write(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: "Reading .env files is not allowed"
        }
    }));
  }
  process.exit(0);
}

main();
```

##### File Step by Step Breakdown

**Lines 2–5 — reading `stdin` in chunks:**
Claude Code passes the tool call data as JSON on `stdin`. Node.js streams data in chunks, so we collect them all into an array and concatenate with `Buffer.concat()` before parsing. You cannot call `JSON.parse` on a partial payload — this pattern ensures we have the complete input before proceeding.

**Line 7 — parsing the tool call object:**
`JSON.parse(Buffer.concat(chunks).toString())` converts the raw buffer into a JavaScript object. The shape is always `{ tool_name, tool_input, ... }`. For the `Read` tool, `tool_input` contains `file_path` — the file Claude is trying to read.

**Lines 9–10 — extracting the path with a fallback:**
Different tools use different field names for paths (`file_path` vs `path`). The `||` chain handles both. If neither field is present, `readPath` becomes an empty string and the `.env` check below will not match — so tools that don't involve files pass through silently.

**Lines 12–19 — writing the deny decision:**
When the path contains `.env`, we write a structured JSON object to `stdout`. `permissionDecision: "deny"` tells Claude Code to block the tool call before it executes. `permissionDecisionReason` is surfaced to the user in the terminal so they understand what blocked the read and why.

**Line 21 — always exit 0:**
A non-zero exit code signals that the hook script itself failed — not that it made a deny decision. If the hook crashes, Claude Code treats it as a hook error, not a policy block. Always exit 0; put your decision entirely in the stdout JSON.

---

#### Python

```python
import sys
import json
import os


def main():
    try:
        tool_args = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = tool_args.get("tool_input", {})

    read_path = (
        tool_input.get("file_path")
        or tool_input.get("path")
        or ""
    )

    normalized_path = os.path.normpath(read_path)
    filename = os.path.basename(normalized_path)

    protected_files = {
        ".env",
        ".env.local",
        ".env.development",
        ".env.production",
        ".env.test",
    }

    if filename in protected_files:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Reading .env files is not allowed",
            }
        }
        sys.stdout.write(json.dumps(output))

    sys.exit(0)


if __name__ == "__main__":
    main()
```

##### File Step by Step Breakdown

**Lines 7–9 — reading stdin with error handling:**
`json.load(sys.stdin)` reads and parses the complete stdin payload in one call. The `try/except` is defensive: if Claude Code sends malformed JSON for any reason, we exit 0 cleanly rather than crashing with a traceback. Exiting 0 without writing any output means the hook has no opinion — the tool call proceeds normally.

**Lines 11–17 — extracting the path:**
Same dual-field fallback as the JavaScript version. The `or ""` at the end guarantees `read_path` is always a string, so the `os.path` calls below never receive `None`.

**Lines 19–20 — normalizing the path:**
`os.path.normpath` resolves `../` traversal segments and redundant slashes — this closes a bypass where a path like `../../task_manager/.env` would avoid a substring match. `os.path.basename` extracts just the filename, so the check targets the filename exactly rather than doing a substring match on the full path. Without this, a file named `dotenv-loader.py` would trip a naive `.env` check.

**Lines 22–28 — the protected files set:**
A Python `set` provides O(1) lookup via `.in`. It covers all standard dotenv variants used by Django, Vite, and Node projects. Adding a new variant requires adding one string — no logic changes.

**Lines 30–38 — writing the deny output:**
Identical in structure to the JavaScript version. `permissionDecision: "deny"` is the blocking signal; `hookEventName` must match the hook type declared in `settings.json`.

**Line 40 — always exit 0:**
Same rule as JavaScript. The deny signal is in the stdout JSON, never in the exit code.

---

### Writing a PostToolUse Hook for Review and Comments

The PreToolUse hook above *blocks* actions. A PostToolUse hook runs *after* a tool completes, which means it can analyze what Claude just did and inject feedback back into the conversation.

Combined with the Anthropic SDK, this creates a second-opinion loop: every time Claude writes or edits a file in the `task_manager`, a separate Claude call reviews the change and surfaces any issues before the next turn.

#### Installing the SDK

```bash
# Python
pip install anthropic

# Node
npm install @anthropic-ai/sdk
```

Both require the `ANTHROPIC_API_KEY` environment variable. The hook runs as a subprocess — ensure your shell environment has the key available:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

#### How the Review Loop Works

```
Claude edits a file in task_manager
             ↓
   PostToolUse hook fires
             ↓
   Hook reads the edited file from disk
             ↓
   Hook calls Claude Haiku with the file content
             ↓
   Review written to stdout as additionalContext
             ↓
   Claude's next turn includes the review in context
```

The `additionalContext` field in the hook's JSON output is injected directly into Claude Code's context before your next message. Claude sees the review as if it had arrived in the conversation — it can respond to flagged issues, revert changes, or continue with awareness of the feedback.

---

#### Python

```python
import sys
import json
import os
import anthropic


def main():
    try:
        tool_args = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = tool_args.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    # Only review source files — skip migrations, configs, lock files
    reviewable = {".py", ".jsx", ".js", ".ts", ".tsx"}
    _, ext = os.path.splitext(file_path)
    if not file_path or not os.path.exists(file_path) or ext not in reviewable:
        sys.exit(0)

    with open(file_path, "r") as f:
        content = f.read()

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": (
                    f"You are a code reviewer. The following file was just edited.\n"
                    f"Identify any bugs, security issues, or clearly missing logic. "
                    f"Be concise — 3 bullet points maximum. If nothing is wrong, say so.\n\n"
                    f"File: {file_path}\n\n```\n{content}\n```"
                )
            }
        ]
    )

    review = message.content[0].text

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": f"[Auto Review: {file_path}]\n{review}"
        }
    }
    sys.stdout.write(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
```

##### File Step by Step Breakdown

**Lines 9–12 — reading the tool call:**
Same stdin pattern as the PreToolUse hook. `tool_input` contains `file_path` for the Write, Edit, and MultiEdit tools — the three tools Claude uses to modify files.

**Lines 14–19 — filtering which files to review:**
Not every file change warrants a review call. Django migrations, `package-lock.json`, and static assets are noisy and expensive to pass through an LLM. The `reviewable` set limits the hook to Python and JavaScript/TypeScript source files — the files where logic errors matter in the task_manager. `os.path.splitext` extracts the extension cleanly. If the file doesn't exist yet or its extension is outside the set, the hook exits silently.

**Lines 21–23 — reading the edited file:**
The hook fires *after* the edit is complete, so the file on disk reflects the new state. Reading it here captures exactly what Claude just wrote.

**Lines 25–40 — the SDK call:**
`anthropic.Anthropic()` initializes the client from `ANTHROPIC_API_KEY` in the environment. We use `claude-haiku-4-5-20251001` — the fastest, cheapest model — because this review fires on *every* file edit. Using Sonnet here would compound costs quickly across a full session. `max_tokens=512` keeps each review fast; the 3-bullet constraint in the prompt enforces focus.

**Lines 42–48 — injecting as context:**
`additionalContext` is what distinguishes PostToolUse from PreToolUse. Instead of blocking, we enrich the next turn. Claude will see `[Auto Review: server/task_app/views.py]` followed by the review before your next message. If the reviewer flags a missing `IsAuthenticated` permission class, Claude already knows about it when you type your next prompt.

---

#### JavaScript

```javascript
import Anthropic from '@anthropic-ai/sdk';
import fs from 'fs';
import path from 'path';

async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }

  let toolArgs;
  try {
    toolArgs = JSON.parse(Buffer.concat(chunks).toString());
  } catch {
    process.exit(0);
  }

  const filePath = toolArgs.tool_input?.file_path || "";
  const reviewable = new Set(['.py', '.jsx', '.js', '.ts', '.tsx']);
  const ext = path.extname(filePath);

  if (!filePath || !fs.existsSync(filePath) || !reviewable.has(ext)) {
    process.exit(0);
  }

  const content = fs.readFileSync(filePath, 'utf8');

  const client = new Anthropic();
  const message = await client.messages.create({
    model: 'claude-haiku-4-5-20251001',
    max_tokens: 512,
    messages: [
      {
        role: 'user',
        content:
          `You are a code reviewer. The following file was just edited.\n` +
          `Identify any bugs, security issues, or clearly missing logic. ` +
          `Be concise — 3 bullet points maximum. If nothing is wrong, say so.\n\n` +
          `File: ${filePath}\n\n\`\`\`\n${content}\n\`\`\``
      }
    ]
  });

  const review = message.content[0].text;

  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PostToolUse',
      additionalContext: `[Auto Review: ${filePath}]\n${review}`
    }
  }));

  process.exit(0);
}

main().catch(() => process.exit(0));
```

##### File Step by Step Breakdown

**Lines 5–15 — streaming stdin and parsing:**
Same chunked-read pattern as the PreToolUse hook. The empty `catch` (no binding) uses ES2019 syntax. On any parse failure the hook exits 0 — a crashing hook would interrupt Claude's workflow, and we prefer silent failure over blocking the agent.

**Lines 17–22 — filtering files:**
`path.extname` returns the extension with the dot (`.py`, `.jsx`). A `Set` provides O(1) `.has()` lookup. `fs.existsSync` guards against the edge case where a tool reports a path for a file that failed to write — without this guard, `readFileSync` would throw and exit with a non-zero code.

**Line 24 — reading the file synchronously:**
`readFileSync` with `'utf8'` encoding returns a plain string. We use the synchronous version deliberately: the subprocess is short-lived and we need the file content before making the API call. There is no meaningful concurrency benefit to the async version here.

**Lines 26–43 — the SDK call:**
`new Anthropic()` reads `ANTHROPIC_API_KEY` from `process.env` automatically. The prompt and constraints are identical to the Python version — same model, same token cap, same 3-bullet instruction.

**Lines 45–51 — injecting context:**
Same `additionalContext` pattern as Python. `hookEventName` must match the hook type registered in `settings.json`.

**Line 53 — top-level error boundary:**
`.catch(() => process.exit(0))` ensures the subprocess never exits non-zero even if the SDK call throws (network error, rate limit, invalid key). The pattern catches any unhandled rejection from the entire `async main()` chain.

---

## Conclusion

Commands, hooks, and the SDK form three layers of project-level control over Claude Code.

**Commands** encode domain knowledge as reusable prompts. Instead of re-explaining the task_manager's two-app Django structure or known security issues every session, you write it once in `.claude/commands/` and invoke it with a slash command.

**Hooks** enforce rules at the agent loop level — below Claude's reasoning. The `.env` PreToolUse hook doesn't ask Claude to respect privacy; it makes the file physically unreachable before Claude's reasoning ever runs. That distinction matters: hooks operate regardless of what Claude decides.

**SDK integration** in PostToolUse hooks turns passive automation into an active feedback loop. Every edit to the task_manager triggers a second, independent Claude call that reviews the change and surfaces issues before you move on. You are using one Claude instance to supervise another.

Together, these tools shift the model from "an AI that responds to prompts" to "a configured agent operating under your project's rules." The next lesson applies all of this to the task_manager directly: reading the codebase, identifying the bugs it contains, and directing Claude Code to fix them with precision.
