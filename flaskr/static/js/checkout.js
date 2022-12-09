document.addEventListener('DOMContentLoaded', () => {
  paypal
    .Buttons({
      style: {
        label: 'pay',
      },
      createOrder: (data, actions) => {
        return actions.order.create({
          purchase_units: [
            {
              amount: {
                currency_code: 'USD',
                value: '100',
              },
            },
          ],
        })
      },
    })
    .render('#paypal-button-container')
})
