describe("Test 3", () => {
  it("Test navigation", () => {
    cy.visit("/film/tt10151854");

    cy.wait(1000);

    cy.get("h2").should("contain.text", "Details");

    cy.get("h3").should("contain.text", "Shazam! Fury of the Gods");

    cy.get(".home-link").click();

    cy.location().should((location) => {
      expect(location.pathname).to.equal("/");
    });
  });
});
