describe("Test 4", () => {
  it("Test navigation", () => {
    cy.visit("/");

    cy.wait(1000);

    cy.get(".inventory-item:first").click();

    // expect the initial state
    cy.get(".checkout-button").should("have.attr", "disabled");

    // can use loops!
    for (let i = 0; i < 4; i++) {
      cy.get(".num-available").should("contain.text", `${i} / 4`);
      cy.get(".return-button").click();
    }

    // check finished state
    cy.get(".num-available").should("contain.text", "4 / 4");
    cy.get(".return-button").should("have.attr", "disabled");

    // check home page reflects the changes
    // [href='/'] is an attribute selector (all selectors are standard css, not unique to cypress)
    cy.get("[href='/']").click();

    cy.get(".inventory-item:first .num-available").should("contain.text", "4");
  });
});
