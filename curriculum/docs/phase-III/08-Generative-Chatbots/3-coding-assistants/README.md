# Coding Assistants

## What are we trying to accomplish?

In this lesson, students move from querying an LLM directly to using one wrapped inside an autonomous agent — a system that can read files, run commands, and iterate on its own until a task is complete. The first lecture explains the architecture that makes this possible: the agent loop, the Model Context Protocol, and why a coding agent is a fundamentally different tool than the LLM it contains. The second lecture turns that understanding into practice: installing Claude Code, configuring a free local model fallback via Ollama, and developing a deliberate decision-making process for model selection based on task complexity and budget. By the end of this lesson, students will have Claude Code running, understand what it is doing under the hood at every step, and be able to make intentional cost-quality trade-offs rather than defaulting to the most powerful model for every task.

## Lectures and Assignments

### Lectures

- [Lecture - Intro to Coding Assistants](./1-intro-to-coding-assistants.md)
- [Lecture - Installing Claude Code](./2-installing-claude.md)

### [Assignments](./assignments.md)

## TLO's (Terminal Learning Objectives)

- Configure and operate Claude Code as a cost-aware coding agent, selecting the appropriate model and effort level for a given development task.

## ELO's (Enabling Learning Objectives)

- Explain the four components of a coding agent: the orchestration loop, MCP servers, tools, and the LLM reasoning core.
- Distinguish between a coding agent and the LLM inside it, and explain why swapping the LLM does not change the agent's orchestration logic.
- Trace the agent loop algorithm from task receipt through sequential tool calls to a final response.
- Explain what the Model Context Protocol (MCP) standardizes and why it matters for tool ecosystem growth.
- Compare GitHub Copilot, Cursor, and Claude Code across use case, transparency, and MCP ecosystem depth.
- Install Claude Code and complete authentication with an Anthropic account or API key.
- Install Ollama and pull a local Qwen3 model as a free fallback for practice sessions.
- Explain what a token is and how input and output tokens are billed in a multi-turn session.
- Select the correct model — Qwen3.5, Haiku, Sonnet, or Opus — given a task's complexity, budget, and internet requirements.
- Configure effort level and output style in Claude Code to balance token cost against reasoning depth and explanation verbosity.
