# Working with LLMs

## What are we trying to accomplish?

In this lesson, students will build a working mental model of how Large Language Models function and how to communicate with them effectively. Starting from the internals of next-token prediction and the Transformer architecture — concepts grounded in the neural network work from the previous module — students will understand what LLMs actually do when they generate a response. From there, the focus shifts to prompt engineering: the discipline of shaping the context you give a model in order to reliably produce useful, accurate, and appropriately formatted outputs. By the end of this lesson, students will be able to write well-structured prompts using the CREF framework, apply named prompting techniques (zero-shot, few-shot, chain-of-thought, role prompting), and correctly diagnose whether a poor model response traces back to a weak prompt or a model limitation.

## Lectures and Assignments

### Lectures

- [Lecture - What are Large Language Models](./1-what-are-llms.md)
- [Lecture - Prompt Engineering](./2-prompt-engineering.md)

### [Assignments](./assignments.md)

## TLO's (Terminal Learning Objectives)

- Write production-quality prompts that reliably produce accurate, well-formatted outputs from a large language model.

## ELO's (Enabling Learning Objectives)

- Explain what a Large Language Model is at a conceptual level, including how next-token prediction produces coherent responses.
- Describe the Transformer architecture and the role of the attention mechanism in enabling models to consider full conversation context simultaneously.
- Distinguish between encoder-only, decoder-only, and encoder-decoder model configurations and identify which category Claude and Gemini fall into.
- Connect the building blocks from module 07 (tokenization, embeddings, neural network training loop) to how LLMs are trained and operate at scale.
- Compare rule-based, retrieval-based, and generative chatbots across response generation strategy, conversation domain, and trade-offs.
- Evaluate Claude, Gemini, and ChatGPT across key dimensions (context window, multimodal support, real-time information, cost, instruction-following) and select the appropriate model for a given task.
- Define prompt engineering and explain why it is a systematic discipline rather than a trial-and-error guessing process.
- Apply the CREF framework (Clarity, Role/Context, Examples, Format) to evaluate and improve a given prompt.
- Recognize the five common bad prompt patterns (too vague, missing context, contradictory, overloaded, assumed knowledge) and rewrite them.
- Apply zero-shot, few-shot, chain-of-thought, and role/persona prompting techniques to appropriate task types.
- Diagnose a poor model response by determining whether the root cause is a prompt failure (fixable by iteration) or a model limitation (hallucination, knowledge cutoff, context window limits, capability ceiling).
- Iteratively refine prompts across a multi-step scenario, observing how each refinement changes response quality.
