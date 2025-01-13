import '../../support/e2e';

describe('Product Detail Page', function () {

  before(() => {
    cy.createProduct();
  });

  it('should contain a link with the open-image-modal class', function () {
    cy.visit('/detail/d3e8b6b1e5a14b6b8b1e5a14b6b8b1e5'); // Use the product ID created in the custom command
    cy.get('a.open-image-modal').should('exist');
  });

});