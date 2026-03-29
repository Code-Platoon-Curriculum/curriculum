# Prompt Engineering

## Introduction

In the last lesson you built a mental model of what an LLM actually is: a system that generates text token by token, each token chosen based on everything that came before it in the conversation. That "everything before it" is the **context window** — and the most important thing you control in that context window is your **prompt**.

This is the core insight behind prompt engineering: *you're not programming logic, you're shaping context.* The model will always generate the most statistically likely continuation of what you gave it. If you give it a vague, ambiguous setup, you'll get a vague, generic continuation. If you give it a precise, well-structured setup, you'll get a focused, useful continuation.

In this lesson you'll learn how to write prompts that reliably get what you need — and how to recognize and debug situations when they don't.

---

## Lesson

### What is Prompt Engineering?

**Prompt engineering** is the practice of designing and refining inputs to a language model in order to reliably produce useful, accurate, and appropriately formatted outputs.

The word "engineering" is intentional. This isn't about guessing magic words or finding tricks. It's a discipline — iterative, systematic, and grounded in an understanding of how models actually work.

Think of it like writing a function signature. If you pass `sort(list)` with no additional context, the function makes assumptions. If you pass `sort(list, key=lambda x: x['age'], reverse=True)`, you get exactly what you need. A prompt is your interface to the model's capabilities — the more precisely you specify the inputs, the more predictable the outputs.

The practice emerged as a distinct skill when it became clear that **the same model could produce dramatically different results depending on how it was asked**. Two people asking GPT-4 to "explain recursion" might get a terse two-line answer or a detailed tutorial with code examples — not because the model changed, but because one prompt gave it more context to work with.

> Prompt engineering doesn't change the model. It changes what the model knows about your task when it starts generating.

---

### Why is the *right* Prompt Important?

Consider two prompts sent to the same model:

**Prompt A:**

```txt
Explain databases.
```

**Prompt B:**

```txt
You are a senior backend engineer explaining database concepts to a junior developer
who has only worked with Python scripts and JSON files so far. Explain what a relational
database is, why it's useful, and how it compares to storing data in flat files.
Keep your explanation under 300 words and use one concrete analogy.
```

Both prompts ask about databases. Prompt B will produce a significantly more useful response — not because it's longer, but because it eliminates *ambiguity*. The model no longer has to guess the audience, the scope, the format, or the appropriate depth.

There are four concrete reasons why the right prompt matters:

**1. Precision**
LLMs fill in ambiguity with assumptions. When your prompt is vague, the model chooses what to assume — and those assumptions may not match what you actually need.

**2. Consistency**
In production systems, prompts are called programmatically, often hundreds or thousands of times. A well-engineered prompt produces consistent, predictable output. A vague prompt produces high variance — sometimes great, sometimes wrong.

**3. Cost**
LLMs are billed by token. A prompt that forces the model to produce a 3,000-token response when 300 words would have sufficed wastes money at scale. Prompts that specify length, format, and scope keep output lean.

**4. Correctness**
A well-scoped prompt reduces the surface area for hallucination. If the model knows exactly what domain it's operating in, it's less likely to wander into territory where it produces confidently wrong information.

---

### What Defines a GOOD vs BAD Prompt?

Good prompts share four properties. Think of the acronym **CREF**:

| Property | What it means |
|---|---|
| **C — Clarity** | The task is specific and unambiguous. The model knows exactly what you're asking for. |
| **R — Role / Context** | You've told the model who it is, what background the user has, or what constraints apply. |
| **E — Examples** | When format or style matters, you've shown the model what good looks like (few-shot prompting). |
| **F — Format** | You've specified what shape the output should take: a list, a paragraph, JSON, code, a table. |

#### Anatomy of a Good Prompt

```txt
[Role / Persona]
You are a software engineering instructor teaching junior developers.

[Context]
The student just learned about for loops in Python and is now seeing list 
comprehensions for the first time.

[Task]
Explain list comprehensions step by step, starting from the equivalent for loop,
and then showing the compressed syntax.

[Format]
Use a code block for each example. Keep the explanation under 200 words.

[Constraint]
Do not use lambda functions or any concepts beyond basic iteration.
```

Not every prompt needs all five components — but every prompt should have at least **Clarity** and **Context**. The more your task requires consistency or formatting, the more the other components matter.

#### Anatomy of a Bad Prompt

Bad prompts share predictable failure patterns:

| Pattern | Example | Problem |
|---|---|---|
| **Too vague** | `"Help me with my code"` | The model doesn't know the language, the problem, or what "help" means |
| **Missing context** | `"Is this good?"` | Good for what? Compared to what standard? |
| **Contradictory** | `"Be brief but explain everything thoroughly"` | The model has to arbitrarily pick one |
| **Overloaded** | `"Write a function, add comments, refactor for performance, and write unit tests"` | Multiple goals compete; none get full attention |
| **Assumed knowledge** | `"Fix the bug"` (no code provided) | The model invents a plausible scenario rather than addressing your actual situation |

#### Prompting Techniques

Beyond structure, there are a few named techniques worth knowing:

**Zero-Shot Prompting** — Ask the model to complete a task with no examples. Works well when the task is common and well-defined.

```txt
Translate the following sentence to Spanish: "The server returned a 404 error."
```

**Few-Shot Prompting** — Provide two or three examples of input → output before asking the model for a new result. Dramatically improves consistency for formatting or classification tasks.

```txt
Classify the following feedback as Positive, Negative, or Neutral.

"The onboarding was smooth." → Positive
"It crashed on startup." → Negative
"I used it once." → Neutral

"The documentation could use more examples." → Positive
```

**Chain-of-Thought (CoT) Prompting** — Ask the model to reason step by step before giving a final answer. Improves accuracy on multi-step reasoning, math, and debugging tasks.

```txt
A Django view is returning a 500 error when a POST request comes in but works fine
for GET requests. Think through the most likely causes step by step, then suggest
a debugging strategy.
```

**Role / Persona Prompting** — Assign the model a role to anchor its tone, vocabulary, and level of detail to a specific perspective.

```txt
You are a security auditor reviewing a junior developer's code. Identify any
potential vulnerabilities in the following Python function.
```

**System Prompts** — In API and product contexts, a *system prompt* is a special instruction block that sets persistent behavior across the entire conversation. You'll work with these directly in lesson 2 when you start calling LLM APIs programmatically.

---

### How to Identify a Bad Response from an LLM

When a model gives you something unusable, the first question isn't "how do I fix this?" — it's **"whose fault is it?"** That distinction determines what you do next.

#### Is it your fault?

Most bad responses trace back to the prompt. Look for these signals:

**The response is too general.** You asked "explain APIs" and got a textbook introduction when you needed a code example. The prompt didn't specify depth, audience, or format.

**The response missed the point.** You asked to fix a bug and the model rewrote the entire function. The prompt didn't constrain scope.

**The response is inconsistent across runs.** You're getting different structure or depth each time you send the same prompt. Add formatting instructions and examples to anchor the output.

**The model asked you to clarify.** This is actually a good sign — it means the model detected ambiguity. But it also means your prompt should have provided that context upfront.

**Diagnosis:** If you could imagine two reasonable people interpreting your prompt differently, the model will too. Make the ambiguous parts explicit.

#### Is it the Agent's fault?

Some failures aren't fixable with a better prompt — they're limitations of the model itself:

**Hallucination.** The model generates confident, plausible-sounding information that is factually wrong. Common in specific factual claims (dates, names, statistics, library APIs). This isn't confusion — the model doesn't *know* it's wrong. It's producing the most statistically likely token sequence, and sometimes that sequence is incorrect.

*What to do:* For factual claims that matter, verify independently. Don't trust model-generated code library calls without checking the docs. Use prompts that ask the model to acknowledge uncertainty (`"If you're not certain, say so"`).

**Knowledge Cutoff.** The model's training data has a cutoff date. Events, library versions, API changes, and news after that date don't exist in its knowledge. Asking Claude about a framework released last month will get you plausible-sounding but outdated or fabricated details.

*What to do:* For time-sensitive information, provide the current context yourself — paste in relevant documentation, release notes, or data. This is the foundation of the **Retrieval-Augmented Generation (RAG)** pattern you'll learn later in this phase.

**Context Window Limits.** Every LLM has a maximum context window — the total tokens it can consider at once across your entire conversation. Extremely long conversations or documents can cause earlier context to be truncated or deprioritized.

*What to do:* For long tasks, break them into focused sub-tasks rather than one enormous prompt. Summarize earlier conversation context when needed.

**Model Capability Ceiling.** Some tasks genuinely exceed what a given model does well. Complex multi-step math, niche domain expertise, and sustained multi-hop reasoning are areas where current LLMs struggle regardless of how the prompt is written.

*What to do:* Recognize the ceiling. Use specialized tools (Wolfram Alpha for math, domain-specific fine-tuned models for specialized fields) rather than fighting the model's limitations with prompts.

> If you've refined the prompt multiple times and the response is still wrong in the same way, you're likely hitting a model limitation. Change your approach — don't keep rewording the same request.

---

### Experiment with Iterative Prompting

Now it's time to experience this firsthand. Open **ChatGPT**, **Gemini**, and **Claude** in separate browser tabs. You'll run two scenarios — each one using **6 iterative prompts** that progressively refine the result. Your goal is to observe how each refinement changes the output, and to notice which model handles each stage best.

> The point isn't to reach a "perfect" final prompt. The point is to develop an intuition for how specificity, context, and constraints change what you get back.

---

#### Scenario 1: Plan a Birthday Party

Work through these six prompts **in order** in a single conversation. After each response, observe: what did the model assume? What was missing? What was useful?

**Prompt 1 — Vague starting point:**

```txt
Help me plan a birthday party.
```

*Notice: What does the model assume? Age of the birthday person? Budget? Number of guests? Venue?*

**Prompt 2 — Add the essential constraints:**

```txt
Plan a birthday party for my 8-year-old daughter. There will be 15 kids.
Our budget is $200.
```

*Notice: Does the advice get more specific? What gaps remain?*

**Prompt 3 — Add context and theme:**

```txt
Plan a birthday party for my 8-year-old daughter. There will be 15 kids.
Our budget is $200. The party is on a Saturday afternoon in April. We have a backyard.
She loves dinosaurs. Give me a detailed 3-hour timeline for the event.
```

*Notice: How does the timeline change when the model has location, season, and theme?*

**Prompt 4 — Scope a specific deliverable:**

```txt
Plan a birthday party for my 8-year-old daughter. There will be 15 kids.
Our budget is $200. The party is on a Saturday afternoon in April. We have a backyard.
She loves dinosaurs. Give me a detailed 3-hour timeline for the event. Ensure to
include a shopping list organized by category (food, decorations, activities,
supplies) for this party. Flag anything that can be bought at a dollar store.
```

*Notice: Does organizing by category and adding a constraint ("dollar store") change the output quality?*

**Prompt 5 — Assign a role:**

```txt
You are a professional party planner writing invitations for a client.
Write two versions of a dinosaur-themed birthday invitation for this party:
one formal and one playful. Include all logistics (date, time, location, RSVP).
```

*Notice: How does the persona affect tone and quality?*

**Prompt 6 — Ask for risk analysis:**

```txt
What could go wrong with an outdoor party for 15 eight-year-olds in April,
and what's a contingency plan for each risk?
```

*Notice: Can the model reason about failure modes? Is the advice practical?*

---

#### Scenario 2: Resume Review

Start a **new conversation** for this scenario. You'll use your own resume or a fictional one — the point is the prompting progression, not the resume content.

**Prompt 1 — No context:**

```txt
Review my resume.
```

*Notice: Without the resume text, what does the model do? What assumptions does it make?*

**Prompt 2 — Add the artifact and role:**

```txt
You are an experienced [job title] hiring manager.
Review the following resume for a [job title] position:

[Paste your resume here]
```

*Notice: How does assigning a role change the specificity and tone of the feedback?*

**Prompt 3 — Narrow the scope:**

```txt
You are an experienced [job title] hiring manager.
Review the following resume for a [job title] position:

[Paste your resume here]

Focus only on the skills section. What technologies are commonly expected
for j[job title] that are missing from this resume?
```

*Notice: Scoping to one section produces more actionable feedback than reviewing everything at once.*

**Prompt 4 — Request a rewrite:**

```txt
Rewrite my summary section to be more impactful for [job title].
Keep it under 3 sentences. Use active language and quantify impact where possible.
```
*Notice: Does the model improve on what's there, or does it invent things that weren't in the original?*

**Prompt 5 — Request a structured evaluation:**

```txt
Rate this resume on a scale of 1 to 10 for a junior software engineer role.
Break the score down by: technical skills, project experience, clarity/formatting,
and overall impact. Justify each sub-score with a specific observation.
```

*Notice: Asking for a structured breakdown forces the model to be specific rather than giving a vague overall judgment.*

**Prompt 6 — Anticipate the interviewer:**

```txt
Based on this resume, what are the 5 most likely interview questions a
hiring manager would ask? For each question, explain why they'd ask it.
```

*Notice: How does the model use the resume content to generate contextually relevant questions?*

---

After completing both scenarios, reflect on:

- Which prompts produced the biggest jumps in response quality?
- Where did the model hallucinate or make assumptions you had to correct?
- Did different models (Claude, Gemini, ChatGPT) handle any prompts noticeably better or worse?

---

## Conclusion

Prompt engineering is the discipline of making your intent legible to a model that can only work with the context you give it.

The key takeaways from this lesson:

- **Prompts are context** — the model generates the most likely continuation of everything in its context window. Shape that context deliberately.
- **CREF** — good prompts have Clarity, Role/context, Examples, and Format specifications. You don't always need all four, but you should always consider them.
- **Bad responses have two causes** — a poorly scoped prompt (fixable by you) or a model limitation (fixable by changing your approach, not rewriting the same prompt).
- **Iteration is the workflow** — start with a clear but minimal prompt, observe the response, identify what's missing, and refine. Prompt engineering is not about getting it right the first time.
- **Techniques exist for a reason** — zero-shot, few-shot, chain-of-thought, and role prompting are tools for specific problems. Know when to reach for each one.

In the next module, you'll move from writing prompts manually in a browser to sending them programmatically via an API. The skills you practiced today translate directly — a system prompt in an API call is just a prompt you've engineered to persist across every conversation your application has.
