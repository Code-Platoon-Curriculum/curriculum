# Working with Dev Containers in VS Code

## Introduction

When working in software development, one of the biggest challenges is making sure everyone’s environment is set up correctly. You may have already seen how different operating systems, Python versions, or installed packages can cause problems when trying to run code from another machine. A development container, or **dev container**, solves this problem by giving us a ready-to-use, standardized environment that works the same way for every developer.

Think of it like a “classroom-in-a-box” — no matter what computer you’re using (Mac, Windows, or Linux), once you open the dev container in VS Code, you’ll be working in the exact same setup as your peers and instructors. This makes it easier to focus on learning the material, instead of troubleshooting system differences.

---

## What is a Dev Container

A **dev container** is essentially a pre-configured coding environment that runs inside a lightweight virtualized system called a *container*. Containers are powered by Docker under the hood, but you don’t need to worry about Docker directly — VS Code handles that for you.

Key points to understand:

* A dev container is defined by a set of configuration files (`.devcontainer` folder) that describe what tools, programming languages, and settings should be installed.
* It is reproducible — if the dev container says “install Python 3.11, Node.js, PostgreSQL, and Git,” then everyone who opens it will get exactly that setup.
* It is isolated — the tools and dependencies inside the dev container do not interfere with your host machine.

For this program, the dev containers you’ll use will come preloaded with:

* **Ubuntu** (a popular Linux environment)
* **Python** (for back-end programming and data work)
* **Node & npm** (for JavaScript and front-end tooling)
* **Git & GitHub CLI (gh)** (for version control and working with repositories)
* **PostgreSQL** (a database server running inside the container)

This ensures you always have the same tech stack as your instructors.

---

## Activating a Dev Container within VS Code

Once you have VS Code and Docker installed, working with a dev container becomes simple. Instead of installing and configuring Python, Node, or PostgreSQL directly on your computer, you’ll just tell VS Code: *“Open this project inside a dev container.”* VS Code will then build the container for you in the background.

The important thing to note is that **your code files stay on your machine**, but VS Code runs them *inside* the container environment. That means you can edit normally, but when you run code, it will be executed in the containerized environment.

---

### Example Dev Container

Here is the Dev Container file (devcontainer.json) we will be utilizing within Code Platoon in order to effectively run our Tech Stack:

**Ensure to update the post command where `Student` is the username utilized within your github account and `student@example.com` is the email related to your github account**

```json
{
  "name": "Code Platoon Dev Container",
  "build": {
    "dockerfile": "Dockerfile"
  },
  "features": {
    "ghcr.io/devcontainers/features/python:1": { "version": "3.11" },
    "ghcr.io/devcontainers/features/node:1": { "version": "18" },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "forwardPorts": [5432],
  "postCreateCommand": "git config --global user.name '<Student>' && git config --global user.email '<student@example.com>' && git config --global core.editor 'code'",
  "customizations": {
    "vscode": {
      "extensions": [
        // Python & Django
        "ms-python.python",                // Core Python support
        "ms-python.vscode-pylance",        // Python language server
        "ms-toolsai.jupyter",              // Jupyter notebooks
        "batisteo.vscode-django",          // Django support
        "kevinrose.vsc-python-indent",     // Fixes Python indentation
        "njpwerner.autodocstring",         // Auto-generate docstrings
        "littlefoxteam.vscode-python-test-adapter", // Testing integration

        // Node & React
        "dbaeumer.vscode-eslint",          // JavaScript/TypeScript linting
        "esbenp.prettier-vscode",          // Code formatter
        "xabikos.javascriptsnippets",      // JavaScript snippets
        "dsznajder.es7-react-js-snippets", // React snippets (ES7+)
        "formulahendry.auto-rename-tag",   // Auto rename paired HTML/JSX tags
        "formulahendry.auto-close-tag",    // Auto close tags
        "mgmcdermott.vscode-language-babel", // Better React/JSX syntax highlighting

        // Live Server & Live Share
        "ritwickdey.liveserver",           // Live Server for HTML/CSS/JS
        "ms-vsliveshare.vsliveshare",      // Live Share collaboration

        // PostgreSQL
        "mtxr.sqltools",                   // SQL management GUI
        "microsoft.vscode-database",       // Database support
        "cweijan.vscode-postgresql-client2", // PostgreSQL client

        // Docker & APIs
        "ms-azuretools.vscode-docker",     // Docker integration
        "humao.rest-client",               // REST client for testing APIs

        // Git
        "mhutchie.git-graph",              // Visual Git graph
        "eamodio.gitlens",                 // GitLens for advanced Git features

        // Utilities
        "streetsidesoftware.code-spell-checker" // Spell checker
      ]
    }
  }
}

```

This file tells VS Code:

* Use Ubuntu as the base system.
* Install Python 3.11.
* Install Node.js v18 and npm.
* Install PostgreSQL through a Dockerfile and host a database locally.
* Include Git and the GitHub CLI.

You don’t need to memorize or write this file — instead you can copy and paste it to any directory you will be utilizing to write code. The important thing is to understand **what this configuration does**: it gives you a fully set-up environment without you doing manual installations.

---

#### Handling PostgreSQL

Unfortunately, the ability to host a PostgreSQL DB within a devcontainer becomes a bit more complicated. In order to accomplish installing this part of our Tech Stack we will need to include a separate `Dockerfile` with specific directions on how to build the database. This will build an additional container within the Docker network that will host PostgreSQL and make it accessible to access from within our devcontainer. We will utilize the following Dockerfile to accomplish this:

```Dockerfile
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install PostgreSQL server + client
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y postgresql postgresql-contrib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Environment vars for postgres setup
ENV POSTGRES_USER=vscode \
    POSTGRES_PASSWORD=codeplatoon \
    POSTGRES_DB=vscode

# Create a startup script to initialize the DB
RUN service postgresql start && \
    sudo -u postgres psql -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';" && \
    sudo -u postgres psql -c "ALTER USER ${POSTGRES_USER} WITH SUPERUSER;" && \
    sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};"

EXPOSE 5432

# Start PostgreSQL automatically
CMD ["bash", "-c", "service postgresql start && tail -f /dev/null"]
```

---

### Steps To Host Dev Container within VS Code

Here’s the step-by-step flow students will use to get a dev container running:

1. **Open VS Code** and install the extension called **Dev Containers** (if it’s not already installed).
2. **Move to your work place** Create a directory where you'll store all of your Code Platoon related notes and or code.
3. **Open the folder in VS Code.** utilizing the `code` command.
4. **Create the Dev Container Folder Structure** by creating a directory named `.devcontainer` and storing the example Dev Container we provided inside of it with the name of `devcontainer.json`. Additionally we will create a file named `Dockerfile` to handle our hosting for PostgreSQL.

        ```
        my-project/
        ├── .devcontainer/
        │   ├── devcontainer.json
        │   └── Dockerfile
        │
        ├── main.py
        ├── main.js
        └── README.md
        ```

5. VS Code will detect the `.devcontainer` configuration and prompt: *“Reopen in Container.”* Click that. If it doesn't prompt you with this option, we can conduct the same through the command palette by pressing `cmd + ⇧ + p` and searching/selecting `Dev Containers: Reopen in Container` option.
6. The first time you open the container, VS Code will build the environment — downloading Ubuntu, installing Python, Node, PostgreSQL, and all other tools. (This may take several minutes the first time.)

---

## Confirming Installations

### Python

**Python** is a high-level, general-purpose programming language known for its simplicity, readability, and versatility, making it one of the most popular languages for beginners and professionals alike. Its clean and easy-to-understand syntax allows developers to focus on solving problems rather than worrying about complex code structures. Python supports multiple programming paradigms, including procedural, object-oriented, and functional programming, and it has a vast ecosystem of libraries and frameworks that make it useful for everything from web development and automation to data science, machine learning, and artificial intelligence. Its strong community support and cross-platform nature make Python an essential tool in modern software development.

We can confirm it's installation was successful within our container by running the `python3 --version` on the terminal:

```bash
$ python --version
```

This should provide an output of the following example or above:

```bash
Python 3.11.13
```

### Node

Node (commonly referred to as **Node.js**) is a JavaScript runtime built on Google’s V8 engine that allows developers to run JavaScript code outside of the browser, typically on a server. It provides an event-driven, non-blocking I/O model, which makes it lightweight and efficient for handling concurrent operations like network requests, file system access, and APIs. With Node, developers can build scalable backend services such as web servers, real-time applications, and APIs, all using JavaScript—the same language used on the client side. It also comes with **npm (Node Package Manager)**, the world’s largest ecosystem of open-source libraries, which makes it easier to integrate external tools and frameworks into applications.

We can confirm it's installation by running `node -v` on the terminal:

```bash
$ node -v
```

This should provide an output of the following example or above:

```bash
v18.20.8
```

### Package Management

Package manager tools are programs that help developers install, update, configure, and remove software packages on their system. Instead of manually downloading files, unpacking them, and placing them in the right directories, a package manager automates the process and ensures everything is installed correctly. Package managers also handle **dependencies** — additional libraries or tools that the software needs to run — which saves developers from having to track those manually. Examples include `apt` (for Linux), `Homebrew` (for macOS), `pip` (for Python), and `npm` (for JavaScript/Node.js).

#### pip

`pip` is the most widely used package manager for Python. It allows developers to install and manage Python libraries and frameworks directly from the [Python Package Index (PyPI)](https://pypi.org/), which is a large online repository of open-source Python packages. For example, if you want to use a library like `requests` for making HTTP calls or `pandas` for data analysis, you can run `pip install requests` or `pip install pandas` in your terminal. Pip also makes it easy to uninstall packages, upgrade them, and list all installed Python packages in your current environment.

#### Node Package Manager (NPM)

`npm` stands for Node Package Manager, and it is the default package manager for Node.js. Like `pip`, it allows developers to install and manage packages, but specifically for JavaScript and Node.js projects. Packages are stored in an online registry, and npm installs them into a `node_modules` directory in your project. You might use npm to install tools like `express` (a web framework) or `react` (a front-end library). Additionally, npm provides a way to manage **scripts** that automate tasks, such as building your app or running tests, which makes it an essential tool for modern JavaScript development.

### Git and Github

**Git** is a distributed version control system that lets developers track changes in their codebase, collaborate with others, and manage different versions of a project efficiently. It allows you to create branches, merge code, and roll back to previous states, making teamwork and experimentation safe and organized. **GitHub**, on the other hand, is a cloud-based platform built around Git that provides hosting for repositories along with collaboration tools like pull requests, issues, and project boards. While Git is the tool that manages version control locally and on servers, GitHub acts as a service that makes sharing, reviewing, and managing code with others much easier.

#### Git

We can ensure git is installed within our command line correctly by running the `git -v` on the terminal. This should provide an output similar to the following:

```bash
git version 2.50.1
```

#### Github Command Line Interface

The dev container we've provided will allow you to utilize `gh` from the terminal to interact with your github repositories from your local machines terminal. With that said, you'll need to authenticate with `gh` every time this Dev Container is started. We can start this authentication process by running `gh auth login` on the terminal. This will raise a series of prompts that will require you to interact with [Github](https://github.com), follow the prompts and successfully authenticate with Github.

### PostgreSQL

**PostgreSQL** (often called **Postgres**) is an open-source, powerful, and highly reliable relational database management system (RDBMS) that uses SQL (Structured Query Language) to store, manage, and retrieve data. Known for its strong standards compliance and advanced features, PostgreSQL supports complex queries, transactions, indexing, JSON storage, and even custom data types, making it suitable for both traditional and modern applications. It is designed for scalability and data integrity, handling everything from small projects to large, enterprise-level systems. Because it’s open-source, actively maintained, and extensible, PostgreSQL is widely used in web applications, analytics, and data-driven software where stability and performance are critical.

In order to finish successfully installing PostgreSQL we will need to complete a couple of steps:

- check the current status of `postgresql` by running the following:

    ```
    sudo service postgresql status
    ```

- If postgresql is down, and it likely will be, go ahead and restart the service with the following command:

    ```
    sudo service postgresql restart
    ```

- Now check the status and ensure postgresql is online. You should see an output similar to the following:
  
    ```
    16/main (port 5432): online
    ```

- If you can't achieve this output or you receive some weird error, ensure to inform an instructor through slack as soon as possible so they may assist you in hosting your environment.

---

## Conclusion

Dev containers give you a reliable, consistent, and portable coding environment. Instead of worrying about differences between Windows, Mac, or Linux setups, you’ll all be coding inside the same Ubuntu-based environment with the same tools: Python, Node, Git, GitHub CLI, and PostgreSQL. This means fewer setup headaches, less time wasted on “it works on my machine” issues, and more time focusing on the material of the program.

As you move through your assignments and projects, whenever you see a `.devcontainer` folder, you’ll know: this is where your coding environment lives. Just open it in VS Code, let it build, and you’re ready to go.
