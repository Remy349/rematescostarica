from flaskr import create_app, db

from flaskr.models.person import Person
from flaskr.models.student import Student
from flaskr.models.course import Course
from flaskr.models.change import Change
from flaskr.models.purchase_paypal import PurchasePaypal
from flaskr.models.cycle import Cycle
from flaskr.models.video import Video
from flaskr.models.material import Material

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "person": Person,
        "student": Student,
        "course": Course,
        "change": Change,
        "purchase_paypal": PurchasePaypal,
        "cycle": Cycle,
        "video": Video,
        "material": Material,
    }
