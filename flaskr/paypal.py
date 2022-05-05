import paypalrestsdk
from flaskr import app
from flask import jsonify, request

@app.route("/payment", methods=["POST"])
def payment():
    """ Funcion para iniciar con el proceso de pago """
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": "/payment",
            "cancel_url": "/cursos",
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "curso",
                    "sku": "12345",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1,
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD",
            },
            "description": "Compra para el curso de rematescostarica!"
        }]
    })

    if payment.create():
        print("Payment creted successfully!")
    else:
        print(payment.error)

    return jsonify({ "paymentID": payment.id })

@app.route("/execute", methods=["POST"])
def execute():
    """ Luego de haber ejecutado el metodo de pago se realiza y confirma la transaccion """
    payment = paypalrestsdk.Payment.find(request.form["paymentID"])
    success = False

    if payment.execute({"payer_id": request.form["payerID"]}):
        print("Payment executed successfully!")
        success = True
    else:
        print(payment.error)

    return jsonify({ "success": success })

@app.route("/payment_completed", methods=["GET"])
def payment_completed():
    """
        Luego de haber completado la compra del curso, se agrega un permiso
        especial para que el usuario tenga acceso a los videos del curso.
    """
    return jsonify({ "message": "Compra completa!" })
