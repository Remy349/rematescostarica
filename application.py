from flaskr import create_app, db

from flaskr.models.person import Person
from flaskr.models.student import Student
from flaskr.models.course import Course

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "person": Person,
        "student": Student,
        "course": Course,
    }
