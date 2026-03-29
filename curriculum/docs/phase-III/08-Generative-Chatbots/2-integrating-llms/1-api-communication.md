# Integrating LLMs

![integrate](./resources/integrate.png)

## Introduction

In the last lesson you learned what LLMs are and how to communicate with them through a browser interface. That's useful for experimentation — but it's not how real applications work. Real applications send prompts *programmatically*, receive structured responses, and incorporate AI as a feature inside a larger system.

In this lesson you'll move from the browser to the terminal. You'll learn how to authenticate with a hosted LLM provider, choose the right model for your use case, construct a prompt as code, and send it over an API — all using Python and the Gemini API.

By the end of this lecture you'll have a working Python script that accepts user input, sends it to Gemini, and prints the model's response. That's the foundation every AI-powered application you build in this phase is built on.

---

## Lesson

### End-State

Before writing any code, it helps to be clear about what you're building and why each piece exists. Here's the complete picture of what this lecture produces:

A Python script that:

1. Defines a **mission** for the AI via a system prompt — telling it who it is, what it knows, and how it should respond
2. Selects a specific **model** from the Gemini family
3. **Authenticates** with Google's API using a secret key
4. **Builds a prompt** by combining the system context with a user message
5. **Sends a request** to the Gemini API and prints the response

Each step maps to a decision you'll make every time you integrate an LLM into an application. Let's work through them in order.

#### Actions List

1. Define the mission for the AI
2. Choose your model
3. Authenticate with the API
4. Build your prompt
5. Communicate with the AI

---

### Defining the Mission for AI

The single most important thing you do before writing any API code is deciding what your AI is *for*. This is what separates a useful, focused assistant from a generic chatbot that produces inconsistent, unpredictable output.

Defining the mission means answering three questions:

#### **What do we want it to do?**

Be specific. "Help users with coding questions" is better than "be a helpful assistant." "Answer questions about our product's Python SDK and nothing else" is better still. The more specific the mission, the more consistent the outputs.

#### **How do we want it to behave?**

Tone, persona, level of detail, what it should and shouldn't say. Should it ask clarifying questions or make its best attempt? Should it respond formally or conversationally? Should it always include code examples?

#### **How should it respond?**

Format and structure. Should it use bullet points or prose? Return JSON? Keep responses under a certain length? Include disclaimers? Proactively offer next steps?

#### The System Prompt is How You Define the Mission

In the browser, you typed prompts manually for each conversation. In the API, you define the mission *once* in a **system prompt** — a special instruction block that persists across the entire session. Every user message is interpreted through the lens of the system prompt.

Here's a well-structured system prompt for a coding assistant:

```python
SYSTEM_PROMPT = """
You are a Python programming assistant for junior software developers.

Your role:
- Answer questions about Python syntax, standard library, and common patterns
- Review code snippets and suggest improvements
- Explain error messages with clear, actionable fixes

Your constraints:
- Keep responses concise — under 300 words unless a longer explanation is clearly necessary
- Always include a code example when explaining a concept
- If a question is outside Python programming, politely redirect

Your tone:
- Friendly and encouraging, but technically precise
- Do not add excessive warnings or caveats
"""
```

Notice how this answers all three questions: what it does (Python assistant), how it behaves (concise, code examples, redirect off-topic), and how it responds (under 300 words, code blocks).

> A system prompt is a promise you make to the model about what context it's operating in. The more clearly you define that context, the more reliably it operates within it.

---

### Choosing your Model

Gemini is a family of models, not a single model. Each variant in the family makes a different trade-off between capability, speed, and cost. Choosing the right one for your use case matters — especially when you're paying per token or optimizing for latency.

#### The Gemini Model Family

As of this writing, the main Gemini models you'll encounter are:

| Model | Best For | Context Window | Notes |
|---|---|---|---|
| `gemini-2.5-flash` | Production apps, fast responses | 1M tokens | Best balance of speed and quality |
| `gemini-2.5-flash-lite` | High-volume, cost-sensitive tasks | 1M tokens | Fastest and cheapest; lower reasoning quality |
| `gemini-2.5-pro` | Complex reasoning, long documents | 1M tokens | Most capable in stable family; higher cost and latency |

For this module, **`gemini-2.5-flash`** is the right choice. It's fast, capable, and free within the API's generous rate limits — which makes it ideal for learning.

```python
MODEL_NAME = "gemini-2.5-flash"
```

#### How to Think About Model Selection

The decision tree for model selection is simple:

1. **Does the task involve very long documents or complex multi-step reasoning?** → Use `gemini-3.1-pro-preview`
2. **Is cost or throughput the primary constraint?** → Use `gemini-2.5-flash-lite`
3. **Everything else** → Use `gemini-2.5-flash`

As you build more complex applications, you may run the same request against multiple models and compare outputs — a practice called **model evaluation**. For now, `gemini-2.5-flash` handles everything in this module.

> This information is consistently changing so please ensure to checkout <a href="https://ai.google.dev/gemini-api/docs" target="_">Gemini API Docs</a> for updates!

---

### Installing the Required Packages

Before we start adding content onto our project, we need to install the following two dependencies to our Python environment.

```bash
pip install -q -U google-genai python-dotenv
```

- **`google-genai`** — Google's official Python SDK for Gemini
- **`python-dotenv`** — loads `.env` files into environment variables

---

### Handling Authentication

To use the Gemini API, you need an **API key** — a credential that identifies your application to Google's servers and authorizes API calls against your account.

#### Getting a Gemini API Key

1. Go to <a href="https://aistudio.google.com" target="_">Google AI Studio</a>
2. Sign in with a Google account
3. Click **"Get API key"** in the top nav
4. Create a new key (or use an existing one from a project)
5. Copy the key — it starts with `AIza...`

#### Storing Your Key Safely

**Never hardcode your API key in source code.** If you push a hardcoded key to GitHub, automated scanners will find it within minutes and it will be compromised.

The correct approach is to store it as an **environment variable** within a `.env` file and read it at runtime.

Due to the way Gemini reads api keys, you must store this key within your environment under the variable of `GEMINI_API_KEY` otherwise it will fail to run correctly.

**Step 1 — Create a `.env` file in your project root:**

```bash
# .env
GEMINI_API_KEY=AIzaSy...your-key-here
```

**Step 2 — Add `.env` to your `.gitignore`:**

```bash
# .gitignore
.env
```

**Step 3 — Read the key in Python using `python-dotenv`:**

```python
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env into os.environ

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set. Check your .env file.")
```

This pattern — load from environment, validate it exists, raise clearly if it doesn't — is the standard approach across all API integrations, not just Gemini.

---

### Communicate with AI

Now that you have a model, prompt and API key within your project, we can confidently begin to send requests to *genai* and receive our selected models responses.


```python
client = genai.Client(api_key=api_key)
user_input = input("What is your question?\n")
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=SYSTEM_PROMPT + "\n\nUser question: " + user_input
)
print(response.text)
```

Now our Python script is capable of executing the following:

1. Insert our API key from a safe location to our Python code
2. Create an instance of Client that is authenticated as ourselves.
3. Capture user input regarding Pythonic questions.
4. Send a request to GenAI with the appropriate model, prompt, and user input
5. Print out a response.

---

## Conclusion

You've moved from typing prompts in a browser to sending them programmatically — and that shift matters. Every AI-powered application, from a customer support bot to a code reviewer to a document summarizer, is built on exactly this foundation: a system prompt that defines the mission, a model chosen for the task, secure authentication, and a call that returns a response.

What you built is minimal by design. A single-turn script that takes one question and returns one answer. That's intentional — understanding the simplest version of the loop before adding complexity is how you avoid building on shaky ground.

In the next lesson you'll extend this foundation. You'll learn how to maintain conversation history across multiple turns, adjust model parameters to control response behavior, and structure your code so the AI component is a clean, reusable piece of a larger application — not just a script that runs once and exits.
