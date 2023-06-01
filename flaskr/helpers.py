import string
import secrets

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


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
