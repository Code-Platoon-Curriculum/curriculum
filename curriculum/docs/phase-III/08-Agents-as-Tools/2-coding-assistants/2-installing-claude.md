# Installing Claude Code

![claudeCode](./resources/claude-code-1.png)

## Introduction

In the last lesson you learned the architecture: a coding agent is an LLM inside an orchestration loop with access to tools via MCP servers. Now you install one.

This lesson covers three things: installing Claude Code, configuring it to run on a free local model when cloud API costs matter, and understanding how tokens and model selection affect what you pay and what you get.

## Lesson

### Why Claude Code?

Several coding agents exist — you saw the comparison in the last lesson. We use Claude Code in this course for specific reasons that connect directly to the architecture you just studied:

1. **Terminal-first, transparent loop** — Claude Code runs in your terminal and surfaces its agent loop as it works: you see every file read, every tool call, every decision. This transparency is intentional for learning.
2. **Deep MCP ecosystem** — Anthropic created MCP, so Claude Code has the most mature and extensive MCP server support. More MCP servers means more tools available to the agent.
3. **200K token context window** — Claude can hold significantly more code context than most alternatives, which matters when navigating large codebases.
4. **Local model support via Ollama** — You can route Claude Code through a locally running open-source model (no API costs, no internet required). This makes it practical for extended practice sessions.

#### Installing Claude

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

This script installs the `claude` CLI binary to your system. After installation, run `claude` to launch the agent and complete authentication — you'll log in with your Anthropic account or provide an API key.

Once authenticated, you're running Claude Code against Anthropic's hosted models (Sonnet by default). Everything you type is sent to Anthropic's API and billed by token usage.

---

### Installing Qwen3 with Ollama

Anthropic's hosted models cost money per token. For extended experimentation, practice sessions, or offline development, you can run Claude Code against a local model instead.

#### What is Ollama?

**Ollama** is a runtime for running open-source LLMs directly on your machine. It handles model downloads, memory management, and serves a local API that other tools — including Claude Code — can connect to.

From your perspective: you run `ollama serve`, and you now have an LLM available at `localhost` with no internet and no per-token billing.

#### What is Qwen3

**Qwen3** is an open-source LLM developed by Alibaba Research. The 3.5B parameter variant runs comfortably on consumer hardware and delivers coding assistance quality that's competitive with smaller commercial models. It won't match Claude Sonnet on complex reasoning, but it handles routine coding tasks, syntax questions, and code review well enough for practice.

> Optionally if internet is not a restriction `glm-4.7-flash` is a model that performs extremely well at isolated Agentic coding tasks.

#### Machine Considerations

Before installing, check your hardware:

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| RAM | 8 GB | 16 GB+ |
| Disk space | 4 GB free | 10 GB+ free |
| GPU | Not required | Helpful (speeds inference 3–5x) |

If your machine has less than 8 GB of RAM, Ollama will still work but responses will be slower as the model paginates through memory.

#### Installing Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify the installation:

```bash
ollama --version
```

#### Using Qwen3 with Ollama

Pull the model (downloads ~2 GB of model weights) and start an interactive session to confirm it's working:

```bash
ollama run qwen3-coder
```

Type a test message, then `Ctrl+D` to exit when satisfied.

---

### Launching Claude with Qwen3

Once Ollama is running, launch Claude Code and point it at your local model:

```bash
ollama launch claude --model qwen3-coder
```

Claude Code will now route all requests to your local Qwen3 instance instead of Anthropic's API. The interface is identical — same commands, same workflow — but zero cost and fully offline.

---

### Managing Token Usage

When running against Anthropic's hosted models, every interaction costs tokens. Understanding how tokens work lets you make deliberate decisions about which model to use and how hard to push it.

#### What are Tokens?

A **token** is the smallest unit of text an LLM processes — not a character, not a word, but something in between. Common patterns:

```
"Hello"        → 1 token
"Hello, world" → 3 tokens  (Hello + , + world)
"authentication" → 2 tokens (authen + tication)
" "            → 1 token   (spaces are tokens too)
```

Rough rule of thumb: **1 token ≈ 4 characters ≈ 0.75 words**. A 1000-word essay is approximately 1,300 tokens.

Every API call has an **input token count** (your message + conversation history + tool results) and an **output token count** (the model's response). Both are billed.

#### How are Tokens Measured?

Claude Code shows your token consumption in the session summary. Pay attention to two numbers:

- **Context tokens**: everything sent to the model (grows as conversation history accumulates)
- **Output tokens**: what the model generated (usually much smaller than input)

Long conversations become expensive not because of your latest message, but because every message resends the full conversation history as context.

#### Model Selection

```bash
/model
```

Use the `/model` command inside Claude Code to switch models at any time. Different models make different cost/capability trade-offs:

##### Sonnet 4.6

- **Cost**: Mid-tier (~$3 per million input tokens / ~$15 per million output tokens)
- **Best for**: Most coding tasks — architecture discussions, debugging, code review, refactoring
- **Avoid when**: You need maximum reasoning depth (use Opus) or maximum speed/cost efficiency (use Haiku)

The default model. Use it for the majority of your work.

##### Opus 4.6

- **Cost**: High (~$15 per million input tokens / ~$75 per million output tokens)
- **Best for**: Hard algorithmic problems, complex system design, tasks where you've already tried Sonnet and hit its ceiling
- **Avoid when**: The task is routine — paying 5x for autocomplete is wasteful

Reserve Opus for problems that genuinely require it. You'll recognize these: Sonnet gives vague or inconsistent answers, or the problem involves multi-step reasoning across large contexts.

##### Haiku 4.5

- **Cost**: Low (~$0.80 per million input tokens / ~$4 per million output tokens)
- **Best for**: Simple lookups, syntax checks, quick completions, high-volume scripted usage
- **Avoid when**: The task requires reasoning, context, or judgment — Haiku struggles with nuance

Haiku is a tool for programmatic workflows where you're making many small calls and cost compounds quickly.

##### Qwen3.5

- **Cost**: Free (compute cost is your machine's CPU/RAM)
- **Best for**: Practice, experimentation, offline development, learning without billing pressure
- **Avoid when**: You need production-quality reasoning or are debugging a hard problem — local models at this size still lag commercial models on complex tasks

Use Qwen3.5 when you're exploring, practicing, or don't want to watch the token counter.

---

#### Determining Effort

Claude Code's **effort level** controls how thoroughly it approaches a task before responding:

| Level | Behavior | Use When |
|-------|----------|----------|
| **Low** | Minimal tool use, fast answer | Quick lookups, simple completions, you know what you want |
| **Medium** | Balanced exploration, reads relevant context | Most coding tasks — the default |
| **High** | Comprehensive analysis, broad exploration | Understanding an unfamiliar codebase, complex bugs, refactors with large blast radius |

Higher effort = more tool calls = more tokens consumed = higher cost. Use High intentionally.

---

#### Output Style

Claude Code's **output style** controls how it communicates decisions to you:

- **Default** — Concise. Shows results, minimal explanation. Fast to read.
- **Explanatory** — Explains reasoning behind decisions. Useful when you want to understand *why* it made a change.
- **Learning** — Maximum transparency. Explains every action, connects decisions to concepts, surfaces trade-offs.

Because this is a coding bootcamp meant to run at no cost to you we suggest the following:

```text
MODEL = qwen3.5
EFFORT = High
OUTPUT STYLE = Learning
```

With Learning mode active, Claude Code will explain what it's doing and why at each step. This is slower to read but is the difference between *using* a tool and *understanding* a tool. The goal of this course is the latter.

To configure this, run `/output-style` inside Claude Code and select **Learning**.

---

#### Putting It Together: Model Selection

Before you reach for the `/model` command, you should be able to make that decision logically.

● **Learn by Doing**

**Context:** You now understand the cost and capability trade-offs for each model. Utilizing [TLDRAW](https://www.tldraw.com/) draw out a decision tree that accounts for those trade-offs — the same reasoning you'll apply every time you reach for `/model` in a real session.

**Your Task:** implement a logical decision tree. Return one of: `"qwen3-coder-next"`, `"qwen3-coder"`, `"claude-haiku-4-5"`, `"claude-sonnet-4-6"`, or `"claude-opus-4-6"`.

**Guidance:** Think through the priorities in order — not all conditions are equal weight. A student in practice mode with no budget should always get Qwen even if the task is complex. A high-complexity task with budget available warrants Opus. The remaining cases fall to Haiku or Sonnet. There are multiple valid orderings; what matters is that your logic is consistent and defensible — could you explain each branch to a teammate?

## Conclusion

You've installed Claude Code, configured a free local model fallback via Ollama, and built a mental model for making cost-aware decisions about which model and effort level to use.

The next lesson moves from configuration to practice: we'll start using Claude Code on real codebases and develop workflows for the kinds of tasks you'll encounter as a developer — reading unfamiliar code, debugging, refactoring, and writing tests with an AI agent actively in the loop.
