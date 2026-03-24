# Phase III — AI & Agentic Engineering: 6-Week Curriculum Proposal

## Overview

This proposal outlines a replacement for the existing Phase III curriculum. It introduces students to modern AI-assisted and agentic engineering practices over 6 weeks. Students entering this phase are assumed to have completed Phase I (Fundamentals, OOP, DS&A) and Phase II (Full-Stack: React, Django, PostgreSQL, Docker).

The module is structured as **30 lessons** across 30 instructional days (5 days/week). Each lesson consists of **2 lectures of 60 minutes each**.

---

## Competency Framework

### Enabling Skills (Conceptual)
- LLM literacy: how models are built, trained, and served
- Understanding agents, tool calls, MCP, RAG, and grounding at a conceptual level
- Knowing the landscape: open-source vs. frontier models, major providers
- Code review as a prompting superpower

### Executable Skills
- Effective prompting
- Vibe coding: casual, AI-assisted development as a daily workflow
- Building agentic `skills.md` specification files
- Calling models via API
- Building, composing, and deploying agents

### Tools
- OpenAI API
- Claude Code (VSCode integration)
- OpenClaw (autonomous multi-purpose agents)

---

## Weekly Breakdown

---

### Week 1 — LLM Literacy & The AI Landscape
> **Goal:** Give students the mental model needed to work confidently with AI tools. No code yet — this week is conceptual but critical. Students should finish week 1 able to explain what an LLM is, how it works at a high level, and where the major tools fit in the ecosystem.

| Day | Lesson | Lecture 1 (60 min) | Lecture 2 (60 min) |
|-----|--------|--------------------|--------------------|
| 1 | What is an LLM? | Models, weights, and parameters — what they are and why they matter | Training vs. pretraining: how models learn from data |
| 2 | How LLMs Generate Output | Inference: how a model turns a prompt into a response | Context windows, temperature, and token limits |
| 3 | Grounding & Knowledge Boundaries | What grounding means and why models hallucinate | RAG (Retrieval-Augmented Generation): concept and use cases |
| 4 | Agents, Tool Calls & MCP | Tool calls: giving models the ability to act | Agents and MCP (Model Context Protocol): orchestrating multi-step tasks |
| 5 | The AI Ecosystem | Open-source vs. frontier models: tradeoffs and when to use each | Major providers overview: OpenAI, Anthropic, Google, Meta, Mistral |

---

### Week 2 — Prompting & Vibe Coding
> **Goal:** Students learn the foundational executable skill of the entire module: prompting. They also establish a vibe coding mindset — treating AI as a casual, always-available coding collaborator rather than a search engine.

| Day | Lesson | Lecture 1 (60 min) | Lecture 2 (60 min) |
|-----|--------|--------------------|--------------------|
| 6 | Prompting Fundamentals I | Anatomy of a good prompt: role, context, task, format | Zero-shot, few-shot, and chain-of-thought prompting |
| 7 | Prompting Fundamentals II | Iterative prompting: refining outputs through conversation | Common failure modes and how to correct them |
| 8 | Code Review as a Prompting Skill | Why code review fluency makes you a better prompter | Reviewing AI-generated code: what to look for and how to give feedback |
| 9 | Vibe Coding I | What vibe coding is: AI as a casual development partner | Integrating AI into your day-to-day workflow without over-relying on it |
| 10 | Vibe Coding II | AI-assisted debugging: walking through problems conversationally | AI-assisted refactoring: improving existing code with prompts |

---

### Week 3 — OpenAI API
> **Goal:** Students move from using AI through interfaces to calling it programmatically. By the end of this week they can build a working AI-powered application using the OpenAI API from scratch.

| Day | Lesson | Lecture 1 (60 min) | Lecture 2 (60 min) |
|-----|--------|--------------------|--------------------|
| 11 | Intro to the OpenAI API | API setup, authentication, and making your first call | Understanding the Chat Completions endpoint: messages, roles, and responses |
| 12 | Controlling Model Behavior | Parameters: temperature, max tokens, top_p, stop sequences | System prompts: shaping model personality and constraints via API |
| 13 | Function Calling | What function calling is and why it matters | Defining and calling functions from a model response |
| 14 | Streaming & Conversation State | Streaming responses: building real-time output in the UI | Managing conversation history: stateless APIs and stateful apps |
| 15 | Building an AI-Powered Application | Architecture of an AI app: front-end, back-end, and model layer | Hands-on build: a simple AI-powered tool using Django + OpenAI API |

---

### Week 4 — Claude Code & VSCode Integration
> **Goal:** Students adopt Claude Code as their primary agentic development environment. They learn how to work *with* an AI coding agent rather than just querying it, and they produce their first `skills.md` specification file.

| Day | Lesson | Lecture 1 (60 min) | Lecture 2 (60 min) |
|-----|--------|--------------------|--------------------|
| 16 | Intro to Claude Code | Setup and environment configuration in VSCode | Core commands: how to interact with Claude Code effectively |
| 17 | Claude Code Workflows | Reading and editing code with Claude Code | Running tasks, tests, and terminal commands through Claude Code |
| 18 | Agentic `skills.md` Files I | What a `skills.md` file is: defining agent capabilities and behavior | Anatomy of a well-written skill: inputs, outputs, constraints, examples |
| 19 | Agentic `skills.md` Files II | Writing skills for common dev tasks: code review, scaffolding, refactoring | Testing and iterating on a skill specification |
| 20 | Agentic Coding Patterns | Delegating multi-step tasks to Claude Code | When to guide vs. when to let the agent run: managing autonomy |

---

### Week 5 — Agent Architecture & Deployment
> **Goal:** Students understand what agents are at an architectural level and build their own. By the end of the week they have a deployed agent that can execute multi-step tasks with minimal human input.

| Day | Lesson | Lecture 1 (60 min) | Lecture 2 (60 min) |
|-----|--------|--------------------|--------------------|
| 21 | Agent Architecture | What makes something an agent: perception, reasoning, action loop | Single-agent vs. multi-agent systems: when each applies |
| 22 | Building a Simple Agent | Designing an agent: defining its goal, tools, and decision logic | Implementation: building a task-oriented agent with the OpenAI API |
| 23 | Multi-Step Agent Workflows | Chaining tool calls: building agents that execute sequences of actions | Handling errors and unexpected states in agentic loops |
| 24 | Agent Deployment | Packaging an agent: environment, dependencies, and configuration | Deploying an agent to a server: hosting, endpoints, and basic monitoring |
| 25 | Training & Refining Agents | Evaluating agent performance: what good and bad output looks like | Prompt tuning and skill refinement: improving agents through iteration |

---

### Week 6 — OpenClaw & Autonomous Multi-Purpose Agents
> **Goal:** Students work with fully autonomous, multi-purpose agents. They learn how to compose agents into pipelines and finish the phase with a working autonomous system built end-to-end.

| Day | Lesson | Lecture 1 (60 min) | Lecture 2 (60 min) |
|-----|--------|--------------------|--------------------|
| 26 | Intro to OpenClaw | What OpenClaw is and how it differs from single-purpose agents | Setting up OpenClaw: environment, configuration, and first run |
| 27 | Building with OpenClaw I | Defining agent roles and responsibilities within OpenClaw | Giving agents tools: connecting to APIs, files, and external services |
| 28 | Building with OpenClaw II | Designing multi-agent pipelines: orchestration and handoffs | Handling agent state and memory across a pipeline |
| 29 | Autonomous Agent Design Patterns | Common patterns: supervisor agents, parallel agents, fallback chains | Safety and guardrails: keeping autonomous agents from going off-script |
| 30 | Capstone Integration | End-to-end review: connecting Week 1 concepts to Week 6 tools | Open build session: students extend or connect their agents into a unified system |

---

## Progression Map

```
Week 1          Week 2          Week 3          Week 4          Week 5          Week 6
────────────    ────────────    ────────────    ────────────    ────────────    ────────────
LLM Literacy    Prompting       OpenAI API      Claude Code     Agent Build     OpenClaw
& Ecosystem  →  & Vibe Coding →  Fundamentals →  & skills.md  →  & Deploy     →  & Autonomy
(Conceptual)    (Workflow)      (Programmatic)  (Agentic IDE)   (Architecture)  (Multi-Agent)
```

---

## Notes

- Weeks 1–2 are intentionally tool-light. Students who skip the conceptual foundation tend to use AI tools poorly. The investment here pays off in weeks 3–6.
- Week 3 uses OpenAI's API specifically because its documentation and community are the most accessible entry point for students new to API-level AI work.
- The `skills.md` pattern introduced in Week 4 is a durable skill — it applies regardless of which agentic platform students use after graduation.
- OpenClaw is introduced last because it assumes fluency with prompting, API calls, and agent architecture. Introducing it earlier tends to produce black-box usage rather than genuine understanding.
