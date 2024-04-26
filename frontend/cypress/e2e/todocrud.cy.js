describe('Creating a task', () => {
    // define variables that we need on multiple occasions
    let vidtitle // video title 
    let todotitle // Title of the todo item
    let email // email of the user

    before(function() {
        // create a fabricated user from a fixture
        cy.fixture('task.json')
            .then((user) => {
                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {
                    uid = response.body._id.$oid
                    name = user.firstName + ' ' + user.lastName
                    email = user.email
                })
            })
    })

    beforeEach(function() {
        // enter the main main page

    })

    it('Get the tasks of the cu', () => {
        // make sure the landing page contains a header with "login"
        cy.get('h1')
            .should('contain.text', 'Login')
    })

    it('login to the system with an existing account', () => {
        // detect a div which contains "Email Address", find the input and type (in a declarative way)
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
            // alternative, imperative way of detecting that input field
            //cy.get('.inputwrapper #email')
            //    .type(email)

        // submit the form on this page
        cy.get('form')
            .submit()

        // assert that the user is now logged in
        cy.get('h1')
            .should('contain.text', 'Your tasks, ' + name)
    })

    after(function() {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})