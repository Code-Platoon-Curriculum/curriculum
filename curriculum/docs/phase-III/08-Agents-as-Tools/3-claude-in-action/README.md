# Claude in Action

## What you will Learn

In this lesson, students apply Claude Code to a real writing project — **DevLog**, a personal developer learning journal built with MkDocs — and develop the workflows and configuration practices that separate precise, efficient agent use from expensive, inaccurate guessing. The first lecture covers context management: how to initialize a project with `CLAUDE.md`, target specific files with `@`-references, use planning mode for multi-file tasks, and manage session accuracy over time. The second lecture covers MCP servers: what they are, how to install them, and how to use the Playwright MCP server to give Claude the ability to open DevLog in a real browser and verify that pages, navigation, and search all work correctly. The third lecture covers project-level customization: custom slash commands that encode domain knowledge, PreToolUse hooks that mechanically block access to sensitive files, and PostToolUse hooks that use the Anthropic SDK to call Claude programmatically for automated code review. By the end of this lesson, students will be able to configure a coding agent that operates under their project's specific rules — not just one that responds to prompts.

## Lectures

- [Lecture - Handling Context](./1-handling-context.md): Learn to control what Claude knows at every point in a session — initializing project memory with `CLAUDE.md`, focusing Claude on specific files with `@`-references, planning multi-file tasks before writing anything, and managing context over long sessions.
- [Lecture - MCP Servers](./2-mcp-servers.md): Extend Claude Code with external tools using the Model Context Protocol — install and configure MCP servers, and use Playwright MCP to give Claude a real browser for verifying that DevLog's pages, navigation, and search work correctly.


## [Assignments](./assignments.md)

## TLO's (Terminal Learning Objectives)

- Configure and direct Claude Code on a real full-stack codebase using context management, MCP servers, custom commands, lifecycle hooks, and SDK integration.

## ELO's (Enabling Learning Objectives)

### Handling Context
- Run `/init` on a new project and extend the generated `CLAUDE.md` with project-specific memory instructions using memory mode (`#` prefix).
- Explain the three scopes of `CLAUDE.md` (project, local, global) and when each is appropriate.
- Use `@`-path references to target specific files rather than triggering broad codebase scans.
- Apply planning mode (`Shift+Tab`) for multi-file tasks and thinking mode keywords for deep single-component reasoning.
- Use `/compact`, `/clear`, and `/cost` to manage accuracy and token spend across a long session.

### MCP Servers
- Explain what MCP (Model Context Protocol) is and how MCP servers extend Claude Code with external tool capabilities.
- Distinguish between the three forms an MCP server can expose: tools, resources, and prompts.
- Install an MCP server using `/mcp add` and configure one manually in `.claude/settings.json`.
- Use Playwright MCP to verify page loads, navigation links, post rendering, and search against a live running MkDocs site.
- Identify when to use Playwright MCP versus file inspection with `@`-references for a given verification task.

### Commands, Hooks, and SDK
- Create custom slash commands in `.claude/commands/` that encode project-specific instructions and accept arguments.
- Define PreToolUse hooks in `settings.json` that deny Claude access to sensitive files before the read executes.
- Explain the stdin/stdout JSON contract that hooks use to communicate with Claude Code.
- Write PostToolUse hooks in Python and JavaScript that use the Anthropic SDK to call Claude for automated code review after every file edit.
- Distinguish between PreToolUse (blocking) and PostToolUse (enriching) hook behavior and select the right hook type for a given use case.

### Technologies

<p style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap">
  <a href="https://claude.ai/code" target="_blank">
    <img src="https://img.shields.io/badge/Claude_Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude Code">
  </a>
  <a href="https://playwright.dev/docs/intro" target="_blank">
    <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  </a>
  <a href="https://docs.anthropic.com/en/api/getting-started" target="_blank">
    <img src="https://img.shields.io/badge/Anthropic_SDK-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Anthropic SDK">
  </a>
</p>
