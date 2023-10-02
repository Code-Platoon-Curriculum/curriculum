describe("Test 2", () => {
  it("Test the general Home PAGE structure", () => {
    cy.visit("/");

    cy.get("h1").should("have.text", "Video Store");
    cy.get("h2").should("contain.text", "Inventory");

    // wait for the api calls to complete
    cy.wait(1000);

    cy.get(".inventory-item").should("have.length", 4);

    cy.get(".inventory-item:first > h3").should(
      "contain.text",
      "A Snowy Day in Oakland"
    );

    cy.get(".inventory-item:first > img").should("have.attr", "src");

    cy.get(".inventory-item:first > .num-available").should(
      "contain.text",
      "0 available"
    );
  });
});
