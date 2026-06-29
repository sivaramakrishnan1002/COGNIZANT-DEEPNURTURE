from . import db


class Course(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    code = db.Column(db.String(20), unique=True)

    credits = db.Column(db.Integer)

    department = db.Column(db.String(100))

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "credits": self.credits,
            "department": self.department
        }