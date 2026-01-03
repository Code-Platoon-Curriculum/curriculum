# Managing Workflows

## Intro

In the previous lecture, we learned **what GitHub Actions workflows are** and how they fit into modern CI practices. In this lecture, we move from *conceptual understanding* to **practical management**. By creating a workflow that will execute your Jest test suite anytime you push code onto a feature branch or attempt to generate a Pull Request. This is common practice in todays Software Development and is an imperative skill for new developers to master.

---

## Project Setup

For this lecture we will utilize node project with a Jest test suite. Please ensure to build the following structure:

```sh
.github/
└── workflows/
|    └── hello-world.yml
| Dockerfile
index.js
main.test.js
package.json
```

Now paste the appropriate code onto the correct file:

**`index.js`**

```js
function factorial(num) {
  let product = 1;

  for (let i = num; i > 0; i--) {
    product = product * i;
  }

  return product;
}

module.exports = factorial;
```

**`main.test.js`**

```js
const factorial = require("./index.js");

describe("tests factorial for small numbers", () => {
  test("tests factorial(0) = 1", () => {
    expect(factorial(0)).toBe(1);
  });

  test("tests factorial(1) = 1", () => {
    expect(factorial(1)).toBe(1);
  });

  test("tests factorial(2) = 2", () => {
    expect(factorial(2)).toBe(2);
  });

  test("tests factorial(3) = 6", () => {
    expect(factorial(3)).toBe(6);
  });
});

describe("tests factorial for large numbers", () => {
  test("tests factorial(10) = 3628800", () => {
    expect(factorial(10)).toBe(3628800);
  });

  test("tests factorial(20) = 2432902008176640000", () => {
    expect(factorial(20)).toBe(2432902008176640000);
  });

  test("tests factorial(40) = 8.15915283247898e47", () => {
    expect(factorial(40)).toBe(8.15915283247898e47);
  });
});
```

**`package.json`**

```json
{
  "name": "trial",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "jest"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "type": "commonjs"
}
```

**`Dockerfile`**

```yml
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install --save-dev jest

COPY . .

CMD ["npm", "test"]
```

---

## Creating a New Workflow

Now that the project is verified, we can automate test execution to ensure only code passing tests can be merged onto the main branch. Now at a high level overview our workflow should be rather simple: 

- In *ubuntu*
- copy this project
- set up a node environment
- install dependencies
- execute the test suite


### Workflow Structure

Within the same directory as our previous workflow create a file named `run-tests.yml`

```sh
.github/
└── workflows/
    └── hello-world.yml
    └── run-tests.yml
```

and add the following code:

```yml
name: Run Test Suite

on:
  push:
    branches:
      - dev

  pull_request:
    branches:
      - main

jobs:
  test:
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

#### Breaking Down the Workflow

- **`on:`** defines *when* the workflow runs, which in this case it's anytime a *pull request* is made to main or anytime code is pushed onto the *dev* branch.
- **`jobs:`** defines a unit of work, for now we will only need one, but as our projects evolve so will our workflows.
- **`runs-on:`** specifies the execution environment as the latest version of *Ubuntu*.
- **Steps** mirrors the steps we mentioned before:
    - `actions/checkout@v4`: Copy this repository
    - `actions/setup-node@v4`: Set up a *node* environment
    - `npm install`: Install dependencies
    - `npm install jest`: Installs jest within the project itself
    - `npm test`: Execute the test suite

> **Mental model:**
> GitHub Actions is simply repeating your local workflow in a clean environment.

### How does this signal a failure?

You may ask yourself, well all this is doing is running my test suite, but how does Github actually know to note if a test failure is present? This is due to the way Github actions is designed to close which either evaluates to 0 or 1 (successful or failure). When the code workflow executes a clean test suite provides a *True* message but if a test fails a different value is passed onto the workflow which signals the workflow as a failure. 

---

## Executing A Workflow Multiple Times

There may come a time when you'll want to execute a workflow outside of the *on* parameters your workflow is utilizing as a trigger. Workflows do **not** only run when code is pushed, so don't think you have to generate a new commit to push each time you want your workflow to be executed. Instead Github has provided us a method to simply relaunch a workflow or job at the click of a button.

To enable this, add `workflow_dispatch` to the *on* section of your workflow and you'll see a button become generated for the workflow:

```yml
on:
  workflow_dispatch:
```

Now when you click on the workflow, you'll see a button on the upper right hand corner stating *Re-run all jobs*. This allows you to run workflows on demand, re-run tests without changing code, and debug pipelines safely without having to generate unnecessary commits that you'll have to clean up later.

In professional environments Developers rerun pipelines to validate fixes, CI engineers debug workflows without polluting commit history making manual execution an essential skill for confidence and iteration

---

## Updating Our Workflow

Workflows are **code**, and they should be treated as such, just like when you update your code in a feature branch, a workflow should be updated within the branch it needs in order to execute it's function. When we update our workflow, it should follow a couple of key concepts:

1. Edit workflows locally and tie them to your commit history to ensure there's a living history you of the evolution of this workflow. This allows developers to view the workflows building process and revert to a previous state if necessary.
2. Workflows, just like code, should be reviewed by other developers and should not be assumed to work properly. They should follow the same pipeline of adding a feature branch, generating commits, and generating a Pull Request for review.

> WORKFLOWS are still CODE

---

### Using Docker within our Workflow

You may have noticed this workflow looks extremely similar to our Dockerfile, and pretty much conduct the exact same behavior. Now you may ask yourself why? This is essentially breaking the *Don't Repeat Yourself* principle so there has to be a reason. It is necessary for us to understand the Workflows and Docker Containers are tools that tackle down two different problems:

- *DOCKER*: “How do I package and run my application consistently?”
- *WORKFLOWS*: “When and how should automated checks run on my code?”

This doesn't mean we can't leverage Docker within our workflows though. In real-world codebases, you will see **both approaches**: One utilizing the native CI, and the other utilizing docker. Lets break down when each one should be utilized:

| Native CLI                      | Docker Container                              |
|--------------------------------|-----------------------------------------------|
| Projects are small             | Environment parity is critical                |
| Build times matter             | Native dependencies exist                     |
| Teams want fast feedback       | Production runs in containers                 |
| Docker is not required for testing | You want “works here == works everywhere” |

### Leveraging Docker within Workflows

Github Actions is actually completely prepped and ready to utilize Docker within it. This means that our recipe for running our test suite changes to:

- set up an environment with ubuntu
- copy this project
- build a Docker image from our Dockerfile
- run the Docker container from the image

```yml
name: Run Test Suite

on:
  push:
    branches:
      - dev

  pull_request:
    branches:
      - main

  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -t app-test .

      - name: Run tests in container
        run: docker run app-test
```

Once you push this onto your *dev* branch you'll see the Docker Engine compiling within the the Actions tab. The same outcome will be provided and you can generate a pull request to merge to main.

---

## Conclusion

Managing workflows is about more than just writing YAML—it’s about **trusting automation**.

In this lecture, you learned how to:

* Confirm a project works before adding CI
* Build a workflow that runs an existing test suite
* Understand pass/fail output in GitHub Actions
* Execute workflows automatically and manually
* Control when workflows run
* Apply best practices for updating workflows

With this foundation, students are now ready to move into **containerized workflows**, where Dockerfiles are executed inside GitHub Actions to create fully reproducible CI pipelines.

That’s where professional-grade automation truly begins.
