describe("Test the header", () => {
  it("displays Video Store", () => {
    cy.visit("/");
    cy.get("h1").should("have.text", "Video Store");
  });
});
