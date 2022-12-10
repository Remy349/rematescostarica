document.addEventListener('DOMContentLoaded', () => {
  const paypalButtonTwo = document.getElementById('paypal-button-container-two')

  if (paypalButtonTwo) {
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
                  value: '129',
                  breakdown: {
                    item_total: {
                      currency_code: 'USD',
                      value: '129',
                    },
                  },
                },
                items: [
                  {
                    name: 'Curso pregrabado',
                    unit_amount: {
                      currency_code: 'USD',
                      value: '129',
                    },
                    quantity: '1',
                  },
                ],
              },
            ],
          })
        },
        onApprove: (data, actions) => {
          return actions.order.capture().then(async function (orderData) {
            const res = await fetch('/payment-completed', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                success: orderData.status,
              }),
            })

            const data = await res.json()

            if (data.message === 'SUCCESS') {
              window.location.href = '/'
            }
          })
        },
      })
      .render(paypalButtonTwo)
  }
})
