const stripe = Stripe(stripePublicKey);

const appearance = {
    theme: 'flat',
    variables: {colorPrimaryText: '#262626'}
};


const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');


const form = document.getElementById('payment-form');

// Handle real-time validation errors from the card Element.
cardElement.on('change', function (event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
});

form.addEventListener('submit', function (event) {
    event.preventDefault();

    console.log("Form cardElement", cardElement)


    stripe.createToken(cardElement).then(function (result) {
        console.log("Form result", result)

        if (result.error) {

            // Inform the user if there was an error.
            // var errorElement = document.getElementById('card-errors');
            // errorElement.textContent = result.error.message;
        } else {
            // Send the token to your server.
            stripeTokenHandler(result.token);
        }
    });
});

// Submit the form with the token ID.
function stripeTokenHandler(token) {
    // Insert the token ID into the form so it gets submitted to the server
    var form = document.getElementById('payment-form');
    var hiddenInput = document.createElement('input');
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('name', 'stripeToken');
    hiddenInput.setAttribute('value', token.id);
    form.appendChild(hiddenInput);

    console.log("Submitting")
    // Submit the form
    HTMLFormElement.prototype.submit.call(form)
}
