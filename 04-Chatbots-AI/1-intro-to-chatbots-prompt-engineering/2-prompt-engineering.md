# Intro to Prompt Engineering

## Intro

In this lecture you will learn about AI driven development capabilities and limitations. You will learn how to implement the concept and practice of Prompt Engineering to construct viable code that you can implement within your projects.

## What is Prompt Engineering

Prompt engineering refers to the practice of carefully crafting input instructions or queries to achieve desired outputs from language models like GPT-3.5. This process involves experimenting with different formulations, structures, and keywords to elicit specific responses. Prompt engineering is a valuable strategy when users seek precise or tailored information, generate creative content, or fine-tune the model's behavior for a particular application. However, caution should be exercised in its use, as excessive manipulation may lead to biased or undesired outcomes. Additionally, prompt engineering might not be suitable for tasks that require the model to learn and generalize from diverse inputs, as it can compromise the model's ability to provide unbiased and contextually appropriate responses. Striking a balance between guidance and allowing the model to exhibit its inherent capabilities is crucial to ensuring responsible and effective use of prompt engineering.

## What is an LLM (Large Language Models)

Large Language Models (LLMs) represent a significant advancement in natural language processing, capable of understanding and generating human-like text. There are two main types of LLMs: Base LLMs and Instruction Tuned LLMs.

1. **Base LLM (GitHub_pilot):**
   - Base LLMs, exemplified by models like GitHub_pilot, are pre-trained on vast datasets, learning from diverse sources on the internet. These models develop a broad understanding of language, enabling them to generate contextually relevant text across a wide range of topics. GitHub_pilot, for instance, is trained on code repositories, making it particularly adept at understanding and generating programming-related content.

2. **Instruction Tuned LLM (ChatGPT):**
   - Instruction Tuned LLMs, such as ChatGPT, undergo an additional fine-tuning process to enhance their performance in specific domains or tasks. By providing explicit instructions during training, these models can be tailored for more specialized use cases. ChatGPT, for example, is fine-tuned for conversational contexts, making it well-suited for interactive and dynamic text generation. The fine-tuning process allows developers to guide the model's behavior and customize its responses to better align with specific user requirements.

3. **Differences:**
   - The primary distinction between Base LLMs and Instruction Tuned LLMs lies in their training processes. While Base LLMs learn from a wide array of data sources to build a general understanding of language, Instruction Tuned LLMs undergo targeted fine-tuning to specialize in particular domains or tasks. This specialization allows Instruction Tuned LLMs to provide more contextually relevant and application-specific responses. However, it's essential to strike a balance between customization and maintaining the model's ability to generalize to diverse inputs for responsible and effective use.

## Capabilities and Limitations

Understanding the capabilities and limitations of Instruction Tuned Large Language Models (LLMs) is crucial for effective prompt engineering. Here, we explore both aspects to provide insights for potential prompt engineers:

### *Capabilities:*

1. **Customization for Specific Tasks:**
   - Instruction Tuned LLMs can be fine-tuned to excel in specific domains or tasks. This allows prompt engineers to customize the model's behavior to meet the requirements of a particular application, making them versatile for various use cases.

2. **Contextual Relevance:**
   - These models can generate contextually relevant responses based on the provided instructions. By carefully crafting prompts, prompt engineers can guide the model to produce outputs that align with the desired context or information.

3. **Adaptability to User Preferences:**
   - Instruction Tuned LLMs can be tailored to respond in ways that align with user preferences or the tone required for a specific application. This adaptability enhances user experience and makes the models more versatile.

4. **Improved Performance in Specialized Tasks:**
   - Fine-tuning allows for improved performance in specialized tasks or industries. For instance, a model fine-tuned on medical language can provide more accurate and domain-specific information in healthcare applications.

### *Limitations:*

1. **Sensitivity to Input Formulation:**
   - Instruction Tuned LLMs may exhibit sensitivity to the formulation of input prompts. Small changes in wording or structure can lead to different outputs, requiring careful consideration by prompt engineers to achieve desired results.

2. **Potential for Bias:**
   - Like all language models, Instruction Tuned LLMs can inherit and perpetuate biases present in their training data. Prompt engineers should be aware of this and take precautions to mitigate biases when crafting prompts and evaluating model outputs.

3. **Lack of Real-world Understanding:**
   - While adept at generating contextually relevant text, these models may lack a genuine understanding of the world. They operate based on patterns learned during training, which may result in responses that appear sensible but lack true comprehension.

4. **Challenge with Ambiguous Queries:**
   - Instruction Tuned LLMs can struggle with ambiguous queries or situations where additional context is needed. Prompt engineers should be mindful of this limitation when designing prompts, providing sufficient information for the model to generate accurate responses.

Understanding these capabilities and limitations empowers prompt engineers to make informed decisions when leveraging Instruction Tuned LLMs, ensuring responsible and effective use.

## Good and Bad Practices

In the realm of prompt engineering, the effectiveness of interactions with language models heavily relies on the formulation and structure of prompts. The way prompts are crafted can significantly impact the quality of responses and the overall user experience. Let's delve into some good and bad practices to better understand how to optimize prompt engineering.

### Good Practices

#### 1. **Clarity and Specificity**

*Description:*
Clear and specific prompts contribute to more accurate and relevant responses. When prompts are unambiguous, the model can better understand the user's intent, leading to more meaningful answers.

*Example Prompt:*

```bash
Good Practice:
"Translate the following English sentence into French: 'The quick brown fox jumps over the lazy dog.'"
```

#### 2. **Contextual Information**

*Description:*
Including relevant context in prompts helps the model better grasp the nuances of the query. This is particularly important for tasks that require contextual understanding.

*Example Prompt:*

```bash
Good Practice:
"Given the historical context of the Renaissance, discuss the impact of artistic movements on societal perceptions of beauty and culture during that period."
```

#### 3. **Progressive Prompting**

*Description:*
Dividing complex queries into simpler, progressive prompts can improve the model's ability to generate accurate responses step by step. This approach is useful for multi-step tasks.

*Example Prompt:*

```bash
Good Practice:
Step 1: "List three key features of renewable energy sources."
Step 2: "Explain how these features contribute to environmental sustainability."
```

### Bad Practices

#### 1. **Vagueness and Ambiguity**

*Description:*
Vague or ambiguous prompts can lead to unpredictable and inaccurate responses. It is crucial to provide clear instructions to obtain meaningful results.

*Example Prompt:*

```bash
Bad Practice:
"Tell me about it."
```

#### 2. **Overly Complex Prompts**

*Description:*
Extremely complex prompts may overwhelm the model, resulting in responses that lack coherence or relevance. Keeping prompts concise and focused is key.

*Example Prompt:*

```bash
Bad Practice:
"Considering the amalgamation of post-modernist and existentialist philosophies in the context of contemporary literature, elucidate the existential implications on the characters and plot development in the novels of the 21st century."
```

#### 3. **Overuse of Jargon**

*Description:*
While domain-specific terms are essential, overloading prompts with excessive jargon may confuse the model. Strive for a balance that ensures clarity and understanding.

*Example Prompt:*

```bash
Bad Practice:
"Apply Heisenberg's Uncertainty Principle to elucidate the quantum mechanical behavior of subatomic particles in a magnetic field."
```

## Applying Prompt-Engineering

### Principles and Tactics on building prompts
  
#### 1. Clear and specific instructions

Clear is not short

- **Tactic 1: Use delimiters to ensure the LLM can clearly identify a separation in the prompt**
  - Triple quotes
  - Triple backticks
  - Triple dashes
  - Angle brackets
  - XML tags

```bash
# here we specify where the text begins and ends with ```
Summarize the text delimited by triple backticks into a single sentence.

```{text}```
```

- **Tactic 2: Ask for a structured output like HTML or JSON**

```bash
Generate a list of three made-up book titles along with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
```

- **Tactic 3: Check whether conditions are satisfied check assumptions required to do the task**

```bash
# Here we specifically break down what to do if a condition 
# is met and what to do otherwise along with a specific format
# and an example in which we would like the text to be returned
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
```

- **Tactic 4: Few-shot prompting**

Give examples of successful conditions of  a task and then ask the model to replicate the behavior provided

```python
# Provide a quick example of the behavior you want the LLM to replicate for you 
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
```

#### 2. Give the model time to think

- **Tactic 1: Specify the steps required to complete a task.**

```python
text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
bad_prompt = """
Translate this paragraph into French, give me a list of all the names within the paragraph, and give me a dict with the summary and the names.

{text}
"""
good_prompt = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text:
```{text}```
"""
```

- **Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion**

  - By instructing the LLM to work out its own solution to a problem you are assuring that it wont just make an assumption that something is correct. This is valuable when running word problems and/or mathematical reasoning along with an attempted solution. You can as the LLM to create it's own solution to the problem and compare it to the solution provided, identify errors, and provide constructive feedback.

### LLM Limitations

- Hallucinations = Makes statements that sound plausible but are not actually true. (Probability upon data provided to the LLM)

```python
prompt = f"""
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
"""
```

Boie is a real company but the product is not yet the LLM will still provide a `Hallucinated` answer that it thinks COULD be factual.

- Reducing hallucinations = provide the LLM a specific set of resources it should utilize to populate it's answer and you could even ask its response to come attached with resources.

### Iterative Prompt Development

1. IDEA
2. IMPLEMENTATION (CODE/DATA/PROMPT)
3. EXPERIMENT WITH RESULT
4. ERROR ANALYSIS
5. REPEAT

Prompt guidelines to follow:

- Be clear and specific
- Analyze why result does not give desired output
- Clarify instructions, give more time to think
- Refine prompts with a batch of examples

## Conclusion

In conclusion, our exploration of prompt engineering and its application to Large Language Models (LLMs) underscores the critical balance between customization and generalization for responsible and effective use. We've delved into the distinctive training processes of Base LLMs like GitHub_pilot and Instruction Tuned LLMs such as ChatGPT, recognizing their broad language understanding and specialized fine-tuning advantages. The nuanced discussion on the capabilities and limitations of Instruction Tuned LLMs emphasizes the importance of prompt engineers understanding sensitivities, potential biases, and the models' limitations in real-world comprehension. The discourse on good and bad practices offers actionable insights, promoting clarity, specificity, and contextual relevance in crafting prompts, while cautioning against pitfalls like vagueness or excessive complexity. As we navigate the dynamic landscape of AI-driven development, a thoughtful approach to prompt engineering remains pivotal for maximizing language model potential while ensuring responsible utilization in diverse applications.

## Resources

- [LLM's](https://blog.gopenai.com/an-introduction-to-base-and-instruction-tuned-large-language-models-8de102c785a6)
- [Intro to LLM's](https://roadmap.sh/guides/introduction-to-llms)
