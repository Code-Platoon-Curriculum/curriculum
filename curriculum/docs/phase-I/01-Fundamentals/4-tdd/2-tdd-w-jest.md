# TDD with Jest

## Intro

As JavaScript applications grow beyond single files, ensuring correctness becomes more difficult—and more important. Small logic errors can ripple through an application, causing bugs that are hard to trace and easy to reintroduce. This is where **Test Driven Development (TDD)** becomes a critical professional skill.

In this lesson, we introduce **TDD using Jest**, the most widely adopted testing framework in the JavaScript ecosystem. Just like with Pytest in Python, Jest allows us to write tests that **define expected behavior before implementation**, catch regressions early, and document how our code is supposed to work.

Because JavaScript runs in many environments—browsers, servers, containers—we will also reinforce best practices by running our Jest test suite inside a **Docker container**. This ensures consistent behavior across machines and mirrors how tests are executed in real-world CI/CD pipelines.

By the end of this lesson, you will be able to:

* Write unit tests using Jest
* Organize and manage test files
* Interpret Jest’s assertion syntax and output
* Run JavaScript tests in a containerized environment using Docker

---

## `import/export` syntax

Now before learning about tests we need to become familiarized with JavaScripts ability to call functions from neighboring files. Unfortunately, it is not as simple and straight forward as what we encountered within Python.

### Exporting/Importing a Single Object

Most programs aren't completely contained in a single file, so how do we split them up and reference the contents of one file from another? There are actually two ways to do this in JS, so we will teach the Node way for now, and come back to this topic again when we introduce frontend development in React.

- factorial.js

```js
function factorial(num) {
  let product = 1;

  for (let i = num; i > 0; i--) {
    product = product * i;
  }

  return product;
}
```

- runner.js

```js
factorial(4);
```

This won't work because `runner.js` is totally unaware of a function called factorial, which lives in a completely separate file. Let's fix this with Node's `exports/require` syntax:

- factorial.js

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

- runner.js

```js
const factorial = require("./factorial.js");

factorial(4);
```

Now this works!

> Note: when requiring, the path to the file you want to require from is _relative_ to the file referencing it.

### Exporting/Importing a Multiple Objects

There are some alternatives to this syntax to know about, for example, if we wanted to export multiple things:

- myFaveNums.js

```js
const x = 1;
const y = 2;
const z = 3;

module.exports = { x, y, z };
```

- runner.js

```js
const { x, y, z } = require("./myFaveNums.js");

console.log(x, y, z);
```

Note that we are simply exporting an entire object here and using destructuring with the `require` statement to peel off multiple variables from that singular object.

---

## Adding Jest to our Docker Container

To ensure our tests run consistently across different machines and environments, we will execute Jest inside a Docker container. This allows us to lock in:

* The Node.js version
* Installed dependencies
* Test execution behavior

Just like with Pytest, this container will run Jest as a **one-off command**—once the test suite finishes, the container exits.

---

### Project Structure Example

A simple project structure might look like this:

```bash
.
├── factorial.js
├── factorial.spec.js
├── package.json
├── package-lock.json
└── Dockerfile
```

Jest requires a `package.json` file. If one does not exist yet, initialize it with:

```bash
npm init -y
```


And update `package.json`:

```json
{
  "scripts": {
    "test": "jest"
  }
}
```

---

### Dockerfile for Running Jest

Create a file named `Dockerfile` in the root of the project:

```Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN npm install --save-dev jest

COPY . .

CMD ["npm", "test"]
```

---

### Dockerfile Breakdown

* **FROM node:18-alpine**
  Uses a lightweight Node.js image suitable for testing.

* **WORKDIR /app**
  Sets the working directory inside the container.

* **COPY package*.json ./ & RUN npm install**
  Installs project dependencies (including Jest).

* **COPY . .**
  Copies all project files into the container.

* **CMD ["npm", "test"]**
  Runs the Jest test suite as a **one-off command**.

Once Jest completes, the container stops automatically.

---

### Building and Running the Container

Build the image:

```bash
docker build -t jest-tests .
```

Run the test suite:

```bash
docker run --rm jest-tests
```

* `--rm` removes the container after execution
* Jest output appears directly in your terminal
* Exit codes reflect test success or failure (important for CI)

> **Scenario:**
> This is exactly how automated test runners execute JavaScript tests in production pipelines.

---

## Managing Tests

### Naming Conventions

When writing tests for the *Jest* Testing Framework you'll need to follow a couple of naming conventions

- Directories: must be named `__tests__`.
- Files: files must end with `<var>.test.js` or `<var>.spec.js` where *var* holds a description of the type of tests found within this file.

---

### Writing our first test

Before we can write any tests in Jest, we need to have something to test. Let's create a file `factorial.js` with the contents:

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

Now, we want to write a test spec, a file Jest will 'pick up' to run our test. **By default Jest will look for files with the extension `.spec.js`**, so let's create a file `factorial.spec.js`:

```js
const factorial = require("./factorial.js");

test("tests factorial(4) = 24", () => {
  expect(factorial(4)).toBe(24);
});
```

So what's going on here?

1. we require the function we want to test

2. we use a function automatically provided for us by Jest (no require necessary) called `test`. This takes two arguments, the first a description of the test, and the second a _callback function_ to run the test. A callback function is just a function that takes no arguments that can be called later by the function it is provided to. It seems tricky but this is a common pattern in JS-land.

3. Inside of the callback function we see something funky:

```js
expect(factorial(4)).toBe(24);
```

This is called an `assertion`, Jest provides this as well. `expect` is a function that takes one argument, and this is where we call the function we want to test, which evaluates to `24`. the `.toBe` is a method on the assertion object that tests whether this output matches another value precisely. This might seem more complex than necessary (why not just say `factorial(4) === 24`?) but the `expect` function allows you to write all sorts of tests, not just basic equality but things like 'is this value in that list?' or 'are these two object the exact same object or just have identical contents?' We won't get into those advanced tests for now, but this is how Jest wants us to write our tests.

Now run `npm test` to run `jest`. Much better output than part 1 assignments, right? Now change the `24` to a `23` so it fails. We don't pass now, but we get a clear explanation of what made it fail. This is incredibly useful when testing real applications compared to merely logging true/false.

---

#### Running multiple tests

If you wanted to write more than one test, you could do so like so:

```js
const factorial = require("./factorial.js");

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
```

This works, but there's a way to 'group' tests that is sometimes useful for describing a whole bunch of tests you want to pass to consider that 'test group' successful. We can 'group' tests with the `describe` keyword.

```js
const factorial = require("./factorial.js");

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

`describe` takes a description as its first argument and the second is a callback function with a number of tests. Jest understands `describe` as well and will print things nicely to reflect that this is a group. `describe` blocks can even be nested, so you can have groups within groups within groups if desired.

---

### Skipping tests

Sometimes it's desired to skip a single test, or a block of tests. Jest makes this easy with `xdescribe` and `xtest`. Just add an `x` in front of the test/describe you want to turn off and it will be skipped. This can make debugging your code easier if you know some tests will fail and they are just making it hard to see the tests you currently care about.

```js
const factorial = require("./factorial.js");

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

  // only this test will be skipped in this block
  xtest("tests factorial(3) = 6", () => {
    expect(factorial(3)).toBe(6);
  });
});

// this entire block will be skipped
xdescribe("tests factorial for large numbers", () => {
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

---

## Conclusion

Test Driven Development shifts testing from an afterthought into a **core design tool**. By writing tests first, we clarify requirements, reduce bugs, and gain confidence when refactoring code. Jest provides a powerful yet approachable framework for applying TDD principles in JavaScript projects.

In this lesson, you learned how to:

* Import and export logic across JavaScript files
* Write and organize Jest test files
* Use assertions to validate expected behavior
* Group, skip, and manage test suites
* Run Jest inside a Docker container for consistent execution

These skills directly translate to professional JavaScript development, whether you are building backend services, frontend applications, or automated pipelines. As projects scale, strong testing practices are not optional—they are essential.
