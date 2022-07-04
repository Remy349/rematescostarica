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
                height: 45,
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
                                    const comprarCursoCard = document.getElementById('comprarCursoCard');

                                    comprarCursoCard.innerHTML = `
                                        <div class="comprar__card-img">
                                            <img
                                                src="https://res.cloudinary.com/dajvxg9wj/image/upload/v1656886393/rematescostarica/compra-realizada_embnd0.png"
                                                alt="Compra del curso completada!"
                                                loading="lazy"
                                            />
                                            <h3>¡Gracias por tu compra!</h3>
                                        </div>
                                        <div class="comprar__card-thank">
                                            <p>
                                                Ahora tendras acceso a los videos del curso y otras funciones adicionales,
                                                visita tu perfil para visualizar la lista de videos actual o ve directamente
                                                al apartado del curso y ve los videos libremente!
                                            </p>
                                        </div>
                                        <div class="comprar__card-btns">
                                            <a href="/perfil/${data.username}" class="comprar__card-btn">
                                                Ir a mi perfil
                                            </a>
                                        </div>
                                    `;
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
