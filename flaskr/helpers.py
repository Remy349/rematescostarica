import string
import secrets
from flask import session

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def clear_form_data_session():
    session.pop("firstname", None)
    session.pop("first_lastname", None)
    session.pop("second_lastname", None)
    session.pop("email", None)
    session.pop("phone_number", None)
    session.pop("payment_code", None)


def generate_code():
    letters = string.ascii_letters
    digits = string.digits

    alphabet = letters + digits
    code_length = 14

    code = ""

    for _ in range(code_length):
        code += "".join(secrets.choice(alphabet))

    return code


def allowed_file(filename):
    return "." in filename and \
            filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
