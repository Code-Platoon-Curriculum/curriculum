# Integrating LLMs

## What are we trying to accomplish?

In this lesson, students transition from using LLMs through a browser interface to integrating them programmatically — the way real applications work. Using Python and the Gemini API, students will authenticate with a hosted LLM provider, construct prompts as code, and send them over an API. The second lecture extends this foundation with four production-relevant capabilities: structured outputs that return typed data instead of plain text, multi-turn conversations with persistent message history, multimodal inputs that incorporate images alongside text, and thinking mode for problems requiring deeper reasoning. By the end of this lesson, students will have a working Python integration that reflects the full range of what a real AI-powered feature requires.

## Lectures and Assignments

### Lectures

- [Lecture - Integrating LLMs](./1-api-communication.md)
- [Lecture - Adjusting Your Agent](./2-adjusting-agent.md)

### [Assignments](./assignments.md)

## TLO's (Terminal Learning Objectives)

- Build a Python application that integrates a hosted LLM via API, returning structured data across a multi-turn conversation.

## ELO's (Enabling Learning Objectives)

- Authenticate with a hosted LLM provider by configuring an API key and initializing the SDK client.
- Explain the role of a system prompt and construct one that sets a model's persona, scope, and response constraints.
- Select an appropriate model from the Gemini family based on cost, capability, and task requirements.
- Send a single-turn prompt to the Gemini API and print the model's response.
- Define a structured output schema using Pydantic and configure the API call to return JSON that matches that schema.
- Build a multi-turn conversation by maintaining and passing a message history list across requests.
- Incorporate image inputs into a Gemini API request alongside text prompts.
- Apply thinking mode to a request and explain how extended reasoning affects response quality and token cost.
- Identify when each capability — structured output, multi-turn, multimodal, thinking mode — is the right tool for a given task.
