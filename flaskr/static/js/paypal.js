document.addEventListener('DOMContentLoaded', () => {
    const paypalBtn = document.getElementById('paypal-button');

    if (paypalBtn) {
        paypal.Button.render({
            env: 'sandbox',
            style: {
                color: 'gold',
                shape: 'rect',
                size: 'responsive',
                tagline: false,
                label: 'pay',
            },
            payment: function(data, actions) {
                return actions.request.post('/payment')
                    .then(function(res) {
                        return res.paymentID;
                    })
                ;
            },
            onAuthorize: function(data, actions) {
                return actions.request.post('/execute', {
                    paymentID: data.paymentID,
                    payerID: data.payerID,
                })
                    .then(function(res) {
                        if (res.success === true) {
                            fetch('/payment_completed', {
                                method: 'GET',
                            })
                                .then(res => res.json())
                                .then(data => {
                                    console.log(data);
                                })
                                .catch(error => console.log(error))
                            ;
                        } else {
                            console.log(res.success);
                        }
                    })
                ;
            }
        }, paypalBtn);
    }
});
