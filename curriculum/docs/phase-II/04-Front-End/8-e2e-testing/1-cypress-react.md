# Cypress and React

## Introduction

Testing is a critical part of building reliable, maintainable applications. For React applications using Vite, end-to-end (e2e) testing ensures that your application behaves as expected from the user’s perspective, not just at the component level. In this lecture, we will explore **Cypress**, a popular testing framework for modern web applications, and integrate it into our **PokemonCard project**.

---

## Why Testing

Testing helps catch bugs early, improves confidence in code changes, and ensures features work as intended. Without testing, even small changes in your React app could break functionality, leading to regression issues, poor user experiences, or production failures.

For e2e testing, the focus is on **user behavior**: interactions with forms, navigation between pages, and the full UI flow, rather than just individual components or logic.

---

### Types of Tests

Modern software testing usually involves a combination of the following test types:

#### Unit Tests

* Focus on **individual components or functions**.
* Fast to run and easy to isolate.
* Ensure that logic works correctly for given inputs.
* Example: Testing a `PokemonCard` component renders the Pokémon name correctly.

#### Integration Tests

* Test **how multiple components work together**.
* Moderate speed and complexity.
* Ensure interactions between components don’t break functionality.
* Example: Testing `PokemonForm` + `HomePage` together to confirm that submitting a form adds a new Pokémon card.

#### End-to-End (e2e) Tests

* Test **the entire application flow** from a user perspective.
* Slower and more resource-intensive.
* Ensures the app behaves correctly in real scenarios, including navigation, forms, API calls, and UI interactions.
* Example: Opening the app, adding a Pokémon, clicking "See Details," and confirming the details page displays correct data.

#### Unit vs Integration vs e2e

| Test Type   | Scope                     | Cost   | Speed    | Importance | Priority |
| ----------- | ------------------------- | ------ | -------- | ---------- | -------- |
| Unit        | Single function/component | Low    | Fast     | High       | High     |
| Integration | Multiple components       | Medium | Moderate | High       | Medium   |
| End-to-End  | Full application flow     | High   | Slow     | Critical   | High     |

---

## The Cypress Test Suite

Cypress is a **modern e2e testing framework** designed to make writing, running, and debugging tests for web applications simple and efficient. Unlike traditional testing tools, Cypress runs inside the browser alongside your application, giving **real-time feedback** and **automatic waiting** for elements to appear.

### Why Cypress

* Easy to install and configure with React + Vite.
* Provides a **visual test runner** to watch tests execute in real time.
* Built-in **retry-ability**, waiting for elements to appear without explicit waits.
* Works with modern frameworks like React, Vue, and Angular.
* Supports **network stubbing** to test API-dependent components like our PokemonCard project.

---

### Installing Cypress to the PokemonCard Project

- Install Cypress as a dev dependency:

```bash
npm install cypress --save-dev
```

- Add a script to `package.json` to open Cypress:

```json
"scripts": {
  "cypress:open": "cypress open",
  "cy:run": "npx cypress run --spec"
}
```

- Create a `cypress.config.js` file with the following content

```js
import { defineConfig } from "cypress";

export default defineConfig({
    e2e: {
        baseUrl: "http://localhost:5173/",
        supportFile: false,
    },
    viewportWidth:1024,
    viewportHeight:768,
    video:false,
})
```

- `e2e`: This is a custom configuration object within the `cypress.config.js` file. It's not a built-in Cypress configuration property. In this example:
    - `baseUrl`: It defines the base URL of your application where your tests will run. In this case, it's set to "[http://localhost:5173](http://localhost:5173)" which is where your Vite development server will render the application.
    - `supportFile`: Setting it to `false` disables the use of custom support files, which are typically used to encapsulate reusable testing logic. If you have custom support files, you can specify their paths here.
- `viewportWidth` and `viewportHeight`: These settings define the dimensions of the browser viewport for your tests. In this example, it's set to a width of 1024 and a height of 768 pixels. Adjust these values to match the expected viewport dimensions for your application.
- `video`: It is set to `false` in this example, which disables video recording during test execution. If you want to enable video recording for your tests, set it to `true`.

---

#### Folder and File Structure

Cypress expects a specific folder structure in your project:

```
pokemon-card-app/
├─ cypress/
│  ├─ e2e/           # All your test files go here
│  │  └─ home.cy.js
├─ package.json
├─ cypress.config.js
```

---

#### Writing Your First Test

Create a file `cypress/e2e/home.cy.js` and utilize the same syntax for writing tests that we learned when writing tests in *Jest*:

```javascript
describe('PokemonCard App Home Page', () => {

  it('displays Pikachu on initial load', () => {
    cy.visit('/')
    cy.get('#cardHolder').children().should('have.length', 1);
  });

});
```

Lets break down the test file a bit to ensure we understand what's going on:

- `describe`: used to group a series of tests
- `it`: used to establish a test and the behavior needed to execute it
- `cy.visit('/')`: Opens a browser to the indexed url which according to our *cypress.config.js* this equates to [http://localhost:5173](http://localhost:5173)
- `cy.get("#cardHolder)`: This grabs an element from the current DOM with the id of *cardHolder*
- `children()`: grabs the *children* array from the parent element
- `should()`: conducts the assertion
    - `have.length`: Is the type of assertion to check the length of an iterable object
    - `1`: Is the expected length to evaluate to.

> Note: Cypress tests are **asynchronous by nature**, so Cypress automatically waits for elements and API calls.

---

#### Executing the Test Suite

To run Cypress, **two servers are needed**:

- **Dev server** (Vite) serving your app and currently managed by *Docker*:
- **Cypress test runner** which will be managed by our own Machine:

```bash
npm run cypress:open
```

* Choose the spec file from the Cypress UI.
* Watch tests run in real time.

#### Executing the Test Suite Headless

Additionally you can execute a spec file without opening the Cypress interface and executing it within the terminal. Cypress still conducts the same actions it just does it without opening an interface and with assumed values:

```bash
npm run cy:run <nameOfSpec>
```

> Always ensure the **dev server is running** while Cypress tests execute.

---

## Conclusion

In this lecture, you learned:

* Why testing is essential for React applications.
* The differences between **unit, integration, and end-to-end (e2e) tests**.
* How Cypress provides a modern, user-focused approach to e2e testing.
* How to **install Cypress**, structure your project, and write your first test for the PokemonCard project.
* How to execute the test suite, understanding the need for multiple servers.

In the next lecture, we will dive deeper into **Cypress assertions**, exploring how to verify DOM elements, state changes, and API responses to ensure your PokemonCard app works correctly under all scenarios.
