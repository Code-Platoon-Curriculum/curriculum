# Prepping the Environment

## Introduction

Before we begin building chatbots—whether rule-based, retrieval-based, or generative—we need to establish a clean, reproducible development environment. In machine learning–driven applications, environment consistency is critical. Differences in Python versions, libraries, or tooling can lead to confusing bugs, incompatible dependencies, or inconsistent model behavior.

In this lecture, we will:

- Create and manage a **Python virtual environment**
- Set up **Jupyter Notebook** for experimentation and learning
- Install foundational machine learning libraries including **PyTorch**, **scikit-learn**, **pandas**, and **NumPy**
- Configure **VSCode** for an efficient ML-focused workflow

By the end of this lesson, every student should have a standardized environment capable of supporting the entire chatbot curriculum.

---

## Python Virtual Environment

### What is a Virtual Environment

A **Python virtual environment (venv)** is an isolated workspace that allows you to install Python packages without affecting your system-wide Python installation. Each virtual environment maintains its own versions of libraries and dependencies.

Virtual environments are especially important in machine learning because:

- ML libraries evolve rapidly
- Different projects often require different dependency versions
- Reproducibility is essential for debugging and collaboration

Using a virtual environment ensures that everyone in the class is working with the same tools and avoids the common “it works on my machine” problem.

---

### Creating a Python VENV

We will standardize on **Python 3.13**, using the system-installed `python3` available on both macOS (Homebrew) and Ubuntu (apt).

> Ensure you are in your project directory before running these commands.

```bash
python3 -m venv .venv
```

This command creates a folder named `.venv/` containing an isolated Python interpreter and package manager.

---

### Management Commands

#### Activate the Virtual Environment

```bash
source .venv/bin/activate
```

Once activated, your terminal prompt will change to indicate you are inside the virtual environment.

#### Deactivate the Virtual Environment

```bash
deactivate
```

You should deactivate the environment when switching projects or when you are done working.

---

### VSCode Consideration

VSCode must be explicitly told to use the Python interpreter inside your virtual environment.

**Steps:**

1. Open the project folder in VSCode
2. Press `Cmd + Shift + P` (macOS) or `Ctrl + Shift + P` (Linux)
3. Select **Python: Select Interpreter**
4. Choose the interpreter located at:

```bash
./.venv/bin/python
```

> if this isn't within the provided options, activate your .venv and write `which python3` onto the terminal. Copy the output of the command and enter it as the interpreter path.

This ensures:

* Jupyter uses the correct kernel
* Installed ML libraries are recognized
* Linting and IntelliSense work correctly

---

## Jupyter Notebook

### What is Jupyter Notebook

**Jupyter Notebook** is an interactive computing environment that allows you to combine live code, explanatory text, equations, and visualizations in a single document. Originally developed from the IPython project, Jupyter has become a cornerstone of the data science and machine learning ecosystem.

Jupyter is widely used because it:

* Encourages experimentation and iteration
* Makes data exploration visual and interactive
* Is ideal for teaching, prototyping, and analysis

Throughout this chatbot curriculum, Jupyter Notebooks will be used to explore datasets, prototype models, and understand ML concepts step by step.

---

### Installing Jupyter Notebook into the VENV

Ensure your virtual environment is activated, then install Jupyter:

```bash
pip install notebook ipykernel
```

* `notebook` provides the classic Jupyter interface
* `ipykernel` allows the virtual environment to be used as a kernel

Register the virtual environment with Jupyter:

```bash
python -m ipykernel install --user --name chatbot-venv --display-name "Chatbot VENV"
```

---

### Creating a Jupyter Notebook File

Launch Jupyter file within VSCode by creating a file with the ending of *ipynb*:

```bash
touch my_notebook.ipynb
```

---

#### Connecting a Shell to Your Jupyter Notebook File

Always confirm the kernel in the top-right corner matches your virtual environment. If it does not:

* Click **Kernel**
* Select **Change Kernel**
* Choose **Chatbot VENV**

This prevents dependency mismatches and runtime errors.

---

### Notebook Blocks

#### Markdown Block

Markdown cells are used to write explanations, notes, and documentation. They support headings, lists, code formatting, and images.

Use Markdown blocks to:

* Explain logic
* Document experiments
* Describe results and conclusions

---

#### Python Block

Python cells execute live code. These blocks are used to:

* Load data
* Train models
* Run experiments
* Visualize results

Notebook execution is **stateful**, meaning variables persist across cells. Execution order matters.

---

## PyTorch

### What is PyTorch

**PyTorch** is an open-source deep learning framework widely used in research and industry. It provides tools for building neural networks, training models, and performing tensor computations efficiently.

PyTorch is popular because:

* It uses dynamic computation graphs
* It feels “Pythonic” and intuitive
* It is widely adopted in modern AI research

In this curriculum, PyTorch will be used to explore neural networks and generative chatbot concepts.

---

### Installing PyTorch (CPU-only)

With your virtual environment activated:

```bash
pip install torch torchvision torchaudio
```

This installs the **CPU-only** version of PyTorch, which is sufficient for learning and experimentation.

---

## Scikit-learn

### What is scikit-learn

**scikit-learn** is a machine learning library focused on classical ML algorithms such as classification, regression, clustering, and similarity search.

It is commonly used for:

* Feature extraction
* Text vectorization
* Similarity-based retrieval
* Model evaluation

Retrieval-based chatbots often rely on scikit-learn techniques.

---

### Installing scikit-learn

```bash
pip install scikit-learn
```

---

## Pandas

### What is pandas

**pandas** is a data manipulation and analysis library built on top of NumPy. It introduces the `DataFrame`, a powerful structure for working with tabular data.

pandas is commonly used for:

* Loading datasets
* Cleaning and transforming data
* Preparing data for ML models

---

### Installing pandas

```bash
pip install pandas
```

---

## NumPy

### What is NumPy

**NumPy** is the foundational numerical computing library in Python. It provides efficient array operations and mathematical functions.

Nearly all ML libraries—including PyTorch and pandas—are built on top of NumPy.

---

### Installing NumPy

```bash
pip install numpy
```

---

## requirements.txt

To ensure reproducibility, we track dependencies using a `requirements.txt` file.

Generate it with:

```bash
pip freeze > requirements.txt
```

This file allows anyone to recreate the environment using:

```bash
pip install -r requirements.txt
```

This practice becomes critical when deploying or collaborating on ML projects.

---

## VSCode Extensions

Recommended VSCode extensions for this module:

* **Python** (Microsoft)
* **Jupyter** (Microsoft)
* **Pylance**
* **Python Data Science Extension Pack**

These extensions improve:

* Notebook integration
* Code completion
* Inline documentation
* ML workflow productivity

---

## Conclusion

A well-prepared environment is the foundation of every successful machine learning project. In this lecture, we created an isolated Python 3.13 virtual environment, configured Jupyter Notebook, installed essential ML libraries, and aligned VSCode with our setup. With these tools in place, you are ready to begin building chatbots—from simple rule-based systems to advanced generative models—without friction or configuration issues. In the next lecture, we will begin implementing our first chatbot and explore how conversational logic works in practice.
