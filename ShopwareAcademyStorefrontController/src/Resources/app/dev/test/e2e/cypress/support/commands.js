Cypress.Commands.add('createProduct', () => {
    cy.authenticate('admin', 'test').then((token) => {
        cy.request({
            method: 'POST',
            url: '/api/_action/sync',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: {
                "write": [{
                    "entity": "product",
                    "action": "upsert",
                    "payload": [{
                        "id": "d3e8b6b1e5a14b6b8b1e5a14b6b8b1e5",
                        "name": "Test Product",
                        "productNumber": "TEST-1234",
                        "stock": 100,
                        "price": [{
                            "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
                            "gross": 19.99,
                            "net": 16.80,
                            "linked": false
                        }],
                        "taxId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
                        "active": true,
                        "visibilities": [{
                            "salesChannelId": "98432def39fc4624b33213a56b8c944d",
                            "visibility": 30
                        }]
                    }]
                }]
            }
        }).then((response) => {
            expect(response.status).to.eq(200);
        });
    });
});