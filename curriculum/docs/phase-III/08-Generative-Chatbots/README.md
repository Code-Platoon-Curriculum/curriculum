# Generative Chatbots

## What are we trying to accomplish?

This module takes students from understanding LLMs conceptually to deploying them as autonomous coding agents. The arc is deliberate: students first learn how large language models work and how to communicate with them effectively, then move to integrating an LLM into a real Python application via API, then shift to using a coding agent — Claude Code — as a development tool on a real full-stack project. Each sub-module answers a different version of the same question: *what do you control, and how?* In the first sub-module the answer is prompts. In the second, code. In the third and fourth, the agent's context, tools, rules, and lifecycle hooks. By the end, students can configure and direct a coding agent to read unfamiliar codebases, identify bugs, and execute multi-file changes — with the precision and intentionality of a senior developer, not a user clicking "accept suggestion."

---

## Lessons

1. [Working with LLMs](./1-working-w-llms/README.md)
2. [Integrating LLMs](./2-integrating-llms/README.md)
3. [Coding Assistants](./3-coding-assistants/README.md)
4. [Claude in Action](./4-claude-in-action/README.md)

---

## Module Topics

- Transformer architecture and next-token prediction
- Prompt engineering: CREF framework, zero-shot, few-shot, chain-of-thought, role prompting
- Comparing LLM providers across context window, cost, multimodal support, and instruction-following
- Gemini API authentication and model selection
- Structured outputs with Pydantic schemas
- Multi-turn conversation management and message history
- Multimodal inputs and thinking mode via the Gemini API
- Coding agent architecture: agent loop, MCP, tools, and LLM separation
- Model Context Protocol (MCP) as a standard for tool integration
- Claude Code installation, Ollama local model fallback, and token cost management
- Context window management: `@`-path targeting, planning mode, thinking modes, interrupt, rewind, compact, clear
- Playwright MCP for browser-based UI and security testing
- Custom slash commands in `.claude/commands/`
- PreToolUse and PostToolUse hooks for automated enforcement and review
- Anthropic SDK integration inside hooks for programmatic LLM calls
