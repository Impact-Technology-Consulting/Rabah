const appearance = {
    theme: 'stripe',

    variables: {
        colorPrimary: '#0570de',
        colorBackground: '#ffffff',
        colorText: '#30313d',
        colorDanger: '#df1b41',
        fontFamily: 'Ideal Sans, system-ui, sans-serif',
        spacingUnit: '2px',
        borderRadius: '4px',
        // See all possible variables below
    }
};

// Pass the appearance object to the Elements instance
const elements = stripe.elements({clientSecret, appearance});