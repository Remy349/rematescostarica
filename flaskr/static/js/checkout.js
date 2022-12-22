document.addEventListener('DOMContentLoaded', () => {
  const paypalButton = document.getElementById('paypal-button-container')

  if (paypalButton) {
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
                  value: '164',
                  breakdown: {
                    item_total: {
                      currency_code: 'USD',
                      value: '164',
                    },
                  },
                },
                items: [
                  {
                    name: 'Curso en vivo',
                    unit_amount: {
                      currency_code: 'USD',
                      value: '164',
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
                course_type: 'vivo',
              }),
            })

            const data = await res.json()

            if (data.message === 'SUCCESS') {
              window.location.href = '/'
            }
          })
        },
      })
      .render(paypalButton)
  }
})
