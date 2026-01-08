# GitHub Actions for CI/CD

## Introduction

Now that we understand **where** our React application will be deployed (GitHub Pages), we can focus on **how** that deployment should happen automatically and safely. This lecture introduces **GitHub Actions**, GitHub’s built-in automation platform, and shows how it enables **Continuous Integration (CI)** and **Continuous Deployment (CD)**.

The goal of CI/CD is simple:

> *Every change to our codebase should be automatically tested, verified, and—if safe—deployed without manual intervention.*

By the end of this lesson, students will understand how to build CI/CD pipelines that:

* Run automated test suites
* Block broken code from being merged
* Deploy only verified builds to GitHub Pages

---

## Continuous Integration

### What Is Continuous Integration?

**Continuous Integration (CI)** is the practice of automatically testing and validating code every time a change is introduced.

In CI:

* Developers push code frequently
* Tests run automatically
* Errors are caught early
* Broken code is prevented from reaching production

CI shifts testing from a **manual, last-minute task** into a **continuous safety net**.

---

### Review: Running Test Suites with Pytest and Jest

CI is not introducing new testing concepts—you have already done this past when we built workflows that would test our JavaScript and Python code with test frameworks like Jest and Pytest. Now we are simply just changing our tools to conduct this action. For example:

Previously, wrote workflows like:

```bash
runs-on: ubuntu-latest

steps:
  - name: Checkout repository
    uses: actions/checkout@v4

  - name: Set up Node.js
    uses: actions/setup-node@v4
    with:
      node-version: 18

  - name: Install dependencies
    run: npm install

  - name: Install Jest
    run: npm install jest

  - name: Run tests
    run: |
      npm test || (echo "❌ Tests failed" && exit 1)
```

We are still going to utilize this pattern but rather than utilizing Jest we would run our test suite with Cypress.

---

### Building a CI Workflow for Cypress and React

For our React + Vite projects, Cypress is ideal for CI since we want our tests to mirror a user interacting with our application. It does this by verifying routing, UI behavior, and interactions and it ensures the application *actually works*, not just that functions pass unit tests

#### CI Goals for This Project

Our CI pipeline should:

* Install dependencies
* Build the application
* Start the dev server
* Run the Cypress test suite
* Fail the workflow if any test fails

---

### Example: Cypress CI Workflow

Create the following file in the workflows directory:

```bash
.github/workflows/cypress.yml
```

Lets take it step by step, first we want to name our workflow and then we want to specify this workflow should only be executed if code is pushed onto main or gh-pages and if there is a pull request generated to main.

```yaml
name: Cypress Tests

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main
      - gh-pages
```

Now that our workflow is aware of when to be executed we must define the steps to execute this workflow.  The workflow holds one job which is to execute the cypress test suite within an ubuntu environment.

```yml
jobs:
  cypress-run:
    runs-on: ubuntu-latest
```

The steps to accomplish this task are multiple. First we must copy our project to the container and install our dependencies:

```yml
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install dependencies
        run: npm install
```

Then we must define our `VITE_PROD` environment variable within our github environment and since this code is meant to go into production we would give it a value of true.

```yml
      - name: Set environment variables
        run: echo "VITE_PROD=true" >> $GITHUB_ENV
```

Finally we can run a version of Cypress that will execute our test suite, run the development server and await for the development server to mount virtually.

```yml   
      - name: Run Cypress tests
        uses: cypress-io/github-action@v6
        with:
          browser: chrome
          start: npm run dev
          wait-on: http://localhost:5173/react-trial
```

#### What This Workflow Does

```yml
name: Cypress Tests

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main
      - gh-pages

jobs:
  cypress-run:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install dependencies
        run: npm install

      - name: Set environment variables
        run: echo "VITE_PROD=true" >> $GITHUB_ENV

      - name: Run Cypress tests
        uses: cypress-io/github-action@v6
        with:
          browser: chrome
          start: npm run dev
          wait-on: http://localhost:5173/react-trial
```

1. Runs on every push or pull request
2. Installs dependencies
3. Builds the application
4. Starts the dev server
5. Runs Cypress tests
6. **Fails the workflow if tests fail**

> If the workflow fails, the pull request cannot be merged.

---

## Continuous Deployment

### What Is Continuous Deployment?

**Continuous Deployment (CD)** means that once code passes all tests and merges into the deployment branch, it is **automatically deployed** without manual approval.

No clicking buttons.
No running commands locally.
No guessing if production is broken.

This empowers Development Teams to always keep users interacting with the newest working version of the application that way new features can easily be introduced to the User.

---

### How Did CI/CD Pipelines Come About?

Historically deployments were manual and prone to errors which forced developers to continuously rely on painful rollback procedures and honestly just turned the entire experience of deployment into a very negative one.

This was all drastically decreased (I won't say fixed), thanks to CI/CD pipelines that would automate e2e testing to ensure behaviors were correctly created and to always conduct the same deployment steps with the same environment through automation.

Modern teams deploy **multiple times per day** using CI/CD.

---

### GitHub Pages Deployment Workflow

Now for our deployment workflow, we need to ensure it executes after our CI's success and uploads our dist directory onto Github Pages.

---

### Example: GitHub Pages Deployment Workflow

```bash
.github/workflows/deploy.yml
```

This should only happen after the CI pipelines execution so we will update our `on` section to utilize the `workflow_run` section that looks for the workflow named *Cypress Tests* and checks if it was executed within the main branch which must be pushed onto deployment.

```yaml
name: Deploy to GitHub Pages

on:
  workflow_run:
    workflows: ["Cypress Tests"]
    branches: ["main"]
    types:
      - completed
```

We are no longer just reading documents and/or data from within our github actions container, so we need to ensure that our workflow holds the appropriate *permissions* for writing new content onto our Github Repository.

```yml
permissions:
  contents: write
```

Now we will start to execute this job only if the CI workflow was `successful`. If so we will set up our environment and move onto our steps:

```yml
jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
```

Just like before, we will copy our codebase onto the workflow container, install our dependencies, create our environment variables, and build the `./dist` directory.

```yml
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install dependencies
        run: npm install

      - name: Set production environment
        run: echo "VITE_PROD=true" >> $GITHUB_ENV

      - name: Build project
        run: npm run build
```

Now the deployment process won't be so straight forward anymore. When we deployed through our local machine we were able to authenticate from our previous work in our machine set up. Now within the container we need to provide a way to re-authenticate who we are. The machine is unaware as to who you are and so is Github. We fix this by stating our github related email and username and then adding a `GitHub Token` to our repository. In the following code block replace values wrapped by `"<>"` to the values matching your project.

```yml
      - name: Deploy to GitHub Pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config --global user.email "<github email>"
          git config --global user.name "<github username>"
          REPO="https://x-access-token:${GITHUB_TOKEN}@github.com/<github username>/<git repo name>.git"
          npx gh-pages -d dist -r $REPO
```

**CHECKOUT THE ACTIONS TAB AND WATCH YOUR WORKFLOW EXECUTE**

---

## Conclusion

CI/CD transforms software development from a risky, manual process into a predictable and reliable system. By combining **GitHub Actions**, **Cypress**, and **GitHub Pages**, you now have a professional-grade pipeline that mirrors real-world engineering workflows.

From this point forward:

* Broken code cannot reach production
* Tests act as gatekeepers
* Deployments happen automatically
* Confidence replaces guesswork

This is the same foundation used by modern engineering teams—scaled down for learning, but architected correctly.
