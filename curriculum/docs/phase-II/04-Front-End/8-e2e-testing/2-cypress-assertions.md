# Cypress Assertions

## Introduction

Now that we have set up Cypress and written our first test, it’s time to dive deeper into **Cypress assertions**. Assertions allow you to verify that your application behaves as expected: elements are visible, content is correct, user interactions produce the intended result, and API-driven state changes reflect in the UI.

In this lecture, we will write assertions for the **PokemonCard project**, covering core functionality such as displaying Pokémon, toggling shiny sprites, navigation, and state persistence.

---

## When to Test

End-to-end tests should focus on **user-visible behavior** and critical flows, not implementation details. For example:

* ✅ Test: User can add a Pokémon via the form and see it on the page.
* ✅ Test: User can navigate to a Pokémon details page and see the correct data.
* ❌ Do not test: Internal component state (like a `useState` variable) or isolated functions—this belongs in unit or integration tests.

**Rule of thumb:** e2e tests simulate **real user interactions** and validate outcomes rather than internal implementation.

---

## Current Application Features

Before writing tests, let’s review the **features of our PokemonCard app**:

1. Displays **Pikachu on initial load**.
2. Users can **add Pokémon** via the input form (e.g., Bulbasaur, Charizard).
3. Users can **toggle shiny sprites** on each Pokémon card.
4. Users can **navigate between Home, About, and Pokémon Details pages**.
5. Users can **remove Pokémon** from the list.
6. Pokémon **shiny state persists** across navigation.
7. Clicking “See Details” navigates to the **PokemonDetails page**.

---

## Testing Features

Create a new Cypress spec file, e.g., `cypress/e2e/pokemon.cy.js`, and we’ll structure tests for each feature.

---

### 1. Starting with Pikachu Upon Application Mount

```javascript
describe('PokemonCard App', () => {

  beforeEach(() => {
    cy.visit('/');
  });

  it('displays Pikachu on initial load', () => {
    cy.get('#cardHolder').children().should('have.length', 1);
    cy.get('#cardHolder').contains('Pikachu');
  });

});
```

> **Assertion Explanation:**

* `children().should('have.length', 1)` ensures only one Pokémon exists initially.
* `contains('Pikachu')` verifies the correct Pokémon name is displayed.

---

### 2. Adding Bulbasaur and Charizard Utilizing Input Form

```javascript
it('can add Bulbasaur and Charizard', () => {
  cy.get('input[name="pokemonName"]').type('Bulbasaur');
  cy.get('button[type="submit"]').click();
  cy.get('#cardHolder').contains('Bulbasaur');

  cy.get('input[name="pokemonName"]').clear().type('Charizard');
  cy.get('button[type="submit"]').click();
  cy.get('#cardHolder').contains('Charizard');

  cy.get('#cardHolder').children().should('have.length', 3);
});
```

> This test simulates form input and asserts that **all added Pokémon are displayed**.

---

### 3. Turning Pokémon Shiny

```javascript
it('can toggle shiny on a Pokemon', () => {
  cy.get('#cardHolder button').contains('shine').first().click();
  cy.get('#cardHolder img').first().should('have.attr', 'src').and('include', 'shiny');

  cy.get('#cardHolder button').contains('un-shine').first().click();
  cy.get('#cardHolder img').first().should('have.attr', 'src').and('not.include', 'shiny');
});
```

> Verifies that clicking the **shine/un-shine button** updates the Pokémon sprite accordingly.

---

### 4. Navigation to About, Home, and Pokémon Details Page

```javascript
it('navigates correctly between pages', () => {
  cy.get('nav a').contains('About').click();
  cy.url().should('include', '/about');

  cy.get('nav a').contains('Home').click();
  cy.url().should('eq', `${Cypress.config('baseUrl')}`);

  // Navigate to details page
  cy.get('#cardHolder button').contains('See Details').first().click();
  cy.url().should('include', '/pokemon/');
  cy.get('h2').should('exist'); // Pokemon name displayed
});
```

> Confirms that the **router and links** function as intended.

---

### 5. Removing Pokémon

```javascript
it('can remove a Pokemon', () => {
  cy.get('#cardHolder button').contains('Remove').first().click();
  cy.get('#cardHolder').children().should('have.length', 2); // Pikachu removed
});
```

> Ensures the remove button updates the UI correctly.

---

### 6. Maintaining Pokémon Shiny State

```javascript
it('maintains shiny state after navigation', () => {
  cy.get('#cardHolder button').contains('shine').first().click();
  cy.get('#cardHolder button').contains('See Details').first().click();

  // Return to Home
  cy.get('nav a').contains('Home').click();
  cy.get('#cardHolder button').contains('un-shine').should('exist');
});
```

> This test ensures that **shiny state persists** because state is lifted to App.jsx and shared via `useOutletContext`.

---

## Conclusion

In this lecture, you learned how to:

* Write **Cypress assertions** to validate user interactions in the PokemonCard app.
* Verify **initial state, form interactions, shiny toggling, navigation, and removal**.
* Test **state persistence** across page navigation, ensuring the app behaves as expected.

With these tests, your PokemonCard project is fully covered by end-to-end tests, giving confidence that core features work correctly from the user's perspective.
