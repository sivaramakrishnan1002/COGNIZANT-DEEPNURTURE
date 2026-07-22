import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'courses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float)

    courses = db.relationship('Course', back_populates='department', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'budget': self.budget
        }


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)

    department = db.relationship('Department', back_populates='courses')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'credits': self.credits,
            'department_id': self.department_id
        }


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return jsonify({"service": "Course Service", "port": 5001, "status": "running"})


@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200


@app.route('/api/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(course.to_dict()), 200


@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.get_json() or {}
    if not data.get('name') or not data.get('code') or data.get('credits') is None:
        return jsonify({"error": "Missing required fields: name, code, credits"}), 400

    if Course.query.filter_by(code=data['code']).first():
        return jsonify({"error": f"Course code '{data['code']}' already exists"}), 400

    course = Course(
        name=data['name'],
        code=data['code'],
        credits=data['credits'],
        department_id=data.get('department_id')
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json() or {}
    course.name = data.get('name', course.name)
    course.code = data.get('code', course.code)
    course.credits = data.get('credits', course.credits)
    course.department_id = data.get('department_id', course.department_id)

    db.session.commit()
    return jsonify(course.to_dict()), 200


@app.route('/api/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted successfully"}), 200


@app.route('/api/departments', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments]), 200


@app.route('/api/departments/<int:id>', methods=['GET'])
def get_department(id):
    dept = Department.query.get(id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(dept.to_dict()), 200


@app.route('/api/departments', methods=['POST'])
def create_department():
    data = request.get_json() or {}
    if not data.get('name'):
        return jsonify({"error": "Missing required field: name"}), 400

    dept = Department(
        name=data['name'],
        budget=data.get('budget', 0.0)
    )
    db.session.add(dept)
    db.session.commit()
    return jsonify(dept.to_dict()), 201


@app.route('/api/departments/<int:id>', methods=['PUT'])
def update_department(id):
    dept = Department.query.get(id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404

    data = request.get_json() or {}
    dept.name = data.get('name', dept.name)
    dept.budget = data.get('budget', dept.budget)

    db.session.commit()
    return jsonify(dept.to_dict()), 200


@app.route('/api/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    dept = Department.query.get(id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404

    db.session.delete(dept)
    db.session.commit()
    return jsonify({"message": "Department deleted successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
