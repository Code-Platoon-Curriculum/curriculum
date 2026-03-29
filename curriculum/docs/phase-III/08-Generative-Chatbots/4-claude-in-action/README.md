# Claude in Action

## What are we trying to accomplish?

In this lesson, students apply Claude Code to a real full-stack project — the `task_manager` application — and develop the workflows and configuration practices that separate precise, efficient agent use from expensive, inaccurate guessing. The first lecture covers context management: how to initialize a project with `CLAUDE.md`, keep Claude's attention on the right files, and use planning mode, thinking modes, and session commands to control what Claude knows at every point. It also covers MCP server extension, using Playwright to automate browser-based testing against a live application. The second lecture covers project-level customization: custom slash commands that encode domain knowledge, PreToolUse hooks that mechanically block access to sensitive files, and PostToolUse hooks that use the Anthropic SDK to call Claude programmatically for automated code review. By the end of this lesson, students will be able to configure a coding agent that operates under their project's specific rules — not just one that responds to prompts.

## Lectures and Assignments

### Lectures

- [Lecture - Context and MCP](./1-context-and-mcp.md)
- [Lecture - Commands, Hooks, and SDK](./2-commands-hooks-n-sdk.md)

### [Assignments](./assignments.md)

## TLO's (Terminal Learning Objectives)

- Configure and direct Claude Code on a real full-stack codebase using context management, custom commands, lifecycle hooks, and SDK integration.

## ELO's (Enabling Learning Objectives)

- Run `/init` on a new project and extend the generated `CLAUDE.md` with project-specific memory instructions using memory mode (`#` prefix).
- Explain the three scopes of `CLAUDE.md` (project, local, global) and when each is appropriate.
- Use `@`-path references to target specific files rather than triggering broad codebase scans.
- Apply planning mode (`shift + tab`) for multi-file tasks and thinking mode keywords for deep single-component reasoning.
- Interrupt, rewind, compact, and clear conversation context to manage accuracy and cost across a session.
- Install Playwright MCP and write prompts that verify end-to-end user flows and route protection on a live application.
- Create custom slash commands in `.claude/commands/` that encode project-specific instructions and accept arguments.
- Define PreToolUse hooks in `settings.json` that deny Claude access to sensitive files before the read executes.
- Explain the stdin/stdout JSON contract that hooks use to communicate with Claude Code.
- Write PostToolUse hooks in Python and JavaScript that use the Anthropic SDK to call Claude for automated code review after every file edit.
- Distinguish between PreToolUse (blocking) and PostToolUse (enriching) hook behavior and select the right hook type for a given use case.
