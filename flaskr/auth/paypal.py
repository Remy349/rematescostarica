import os
import base64
import requests
from flaskr import db
from flaskr.auth.email import send_user_information_email
from flaskr.helpers import clear_form_data_session, generate_code
from flask import (
    Blueprint,
    session,
    jsonify,
    redirect,
    request,
    url_for,
)

from flaskr.models.change import Change
from flaskr.models.course import Course
from flaskr.models.person import Person
from flaskr.models.student import Student
from flaskr.models.purchase_paypal import PurchasePaypal

bp = Blueprint("paypal", __name__)


@bp.route("/create-order", methods=["POST"])
def create_order():
    data = request.get_json() or {}

    change = db.session.execute(db.select(Change).filter_by(id=1)).scalar_one()

    course_name = data["courseName"]
    product_price = None

    session["course_name"] = course_name

    api_url = os.getenv("PAYPAL_API_URL_DEV")
    client_id = os.getenv("PAYPAL_CLIENT_ID_DEV")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET_DEV")

    return_url = os.getenv("PAYPAL_RETURN_URL_TEST")
    cancel_url = os.getenv("PAYPAL_CANCEL_URL_TEST")

    access_token = get_access_token(api_url, client_id, client_secret)

    if course_name == "Vivo":
        course_price = 75000
        product_price = course_price // change.change_price
    elif course_name == "Pregrabado":
        course_price = 55000
        product_price = course_price // change.change_price

    json = create_product(
        product_name=course_name,
        product_price=product_price,
        cancel_url=cancel_url,
        return_url=return_url,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.post(
        f"{api_url}/v2/checkout/orders",
        headers=headers,
        json=json,
    )

    return jsonify(response.json())


@bp.route("/capture-order", methods=["GET"])
def capture_order():
    api_url = os.getenv("PAYPAL_API_URL_DEV")
    client_id = os.getenv("PAYPAL_CLIENT_ID_DEV")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET_DEV")

    token = request.args["token"]

    access_token = get_access_token(api_url, client_id, client_secret)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{api_url}/v2/checkout/orders/{token}/capture",
        headers=headers,
    ).json()

    gross_amount = response["purchase_units"][0]["payments"]["captures"][0][
        "seller_receivable_breakdown"
    ]["gross_amount"]["value"]
    paypal_fee = response["purchase_units"][0]["payments"]["captures"][0][
        "seller_receivable_breakdown"
    ]["paypal_fee"]["value"]
    net_amount = response["purchase_units"][0]["payments"]["captures"][0][
        "seller_receivable_breakdown"
    ]["net_amount"]["value"]

    firstname = session.get("firstname")
    first_lastname = session.get("first_lastname")
    second_lastname = session.get("second_lastname")
    email = session.get("email")
    phone_number = session.get("phone_number")
    course_name = session.get("course_name")

    password = generate_code()
    student_code = generate_code()

    course = db.session.execute(
        db.select(Course).filter_by(course_name=course_name)
    ).scalar_one()

    person = Person(
        firstname=firstname,
        first_lastname=first_lastname,
        second_lastname=second_lastname,
        email=email,
    )

    person.is_admin = False
    person.set_password(password)

    student = Student(
        phone_number=phone_number,
        student_code=student_code,
        person=person,
    )

    student.courses.append(course)

    purchase_paypal = PurchasePaypal(
        purchase_gross_amount=gross_amount,
        purchase_paypal_fee=paypal_fee,
        purchase_net_amount=net_amount,
        student=student,
        course=course,
    )

    db.session.add(person)
    db.session.add(student)
    db.session.add(purchase_paypal)
    db.session.commit()

    send_user_information_email(email=email, password=password)

    return redirect(
        url_for(
            "auth.registro_compra_finalizada",
            payment_code=session.get("payment_code"),
        )
    )


@bp.route("/cancel-order", methods=["GET"])
def cancel_order():
    clear_form_data_session()
    return redirect(url_for("main.index"))


def get_access_token(api_url, client_id, client_secret):
    basic_auth = base64.b64encode(
        f"{client_id}:{client_secret}".encode(),
    ).decode()

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic_auth}",
    }

    response = requests.post(
        f"{api_url}/v1/oauth2/token",
        headers=headers,
        data=data,
    ).json()

    return response["access_token"]


def create_product(product_name, product_price, cancel_url, return_url):
    return {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "items": [
                    {
                        "name": f"{product_name}",
                        "description": f"Compra del curso {product_name}",
                        "quantity": "1",
                        "unit_amount": {
                            "currency_code": "USD",
                            "value": f"{product_price}",
                        },
                    },
                ],
                "amount": {
                    "currency_code": "USD",
                    "value": f"{product_price}",
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": f"{product_price}",
                        }
                    },
                },
            }
        ],
        "application_context": {
            "brand_name": "Remates Costa Rica",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": f"{return_url}",
            "cancel_url": f"{cancel_url}",
        },
    }
