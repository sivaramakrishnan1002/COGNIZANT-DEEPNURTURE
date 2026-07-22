import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

COURSE_SERVICE_URL = os.environ.get("COURSE_SERVICE_URL", "http://localhost:5001")


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    enrollments = db.relationship('Enrollment', back_populates='student', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)

    student = db.relationship('Student', back_populates='enrollments')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_id': self.course_id
        }


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return jsonify({"service": "Student Service", "port": 5002, "status": "running"})


@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students]), 200


@app.route('/api/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student.to_dict()), 200


@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json() or {}
    if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
        return jsonify({"error": "Missing required fields: first_name, last_name, email"}), 400

    if Student.query.filter_by(email=data['email']).first():
        return jsonify({"error": f"Student email '{data['email']}' already exists"}), 400

    student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}
    student.first_name = data.get('first_name', student.first_name)
    student.last_name = data.get('last_name', student.last_name)
    student.email = data.get('email', student.email)

    db.session.commit()
    return jsonify(student.to_dict()), 200


@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"}), 200


@app.route('/api/students/<int:id>/enroll', methods=['POST'])
def enroll_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}
    course_id = data.get('course_id') or request.args.get('course_id')
    if not course_id:
        return jsonify({"error": "Missing required parameter: course_id"}), 400

    try:
        course_id = int(course_id)
    except ValueError:
        return jsonify({"error": "course_id must be an integer"}), 400

    # Step 100: Inter-Service call to verify course exists in Course Service
    try:
        response = requests.get(f"{COURSE_SERVICE_URL}/api/courses/{course_id}", timeout=3)
    except requests.exceptions.RequestException as e:
        # Step 101: Handle scenario where Course Service is unavailable
        return jsonify({
            "error": "Course Service Unavailable",
            "details": f"Failed to connect to Course Service: {str(e)}"
        }), 503

    if response.status_code == 404:
        return jsonify({"error": f"Course with ID {course_id} does not exist in Course Service"}), 404
    elif response.status_code != 200:
        return jsonify({
            "error": "Course Service returned an error",
            "status_code": response.status_code
        }), response.status_code

    # Check if already enrolled
    existing_enrollment = Enrollment.query.filter_by(student_id=id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({
            "message": "Student already enrolled in this course",
            "enrollment": existing_enrollment.to_dict()
        }), 200

    enrollment = Enrollment(student_id=id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        "message": f"Student {id} successfully enrolled in course {course_id}",
        "enrollment": enrollment.to_dict(),
        "course": response.json()
    }), 201


@app.route('/api/students/<int:id>/enrollments', methods=['GET'])
def get_student_enrollments(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    enrollments = Enrollment.query.filter_by(student_id=id).all()
    return jsonify([e.to_dict() for e in enrollments]), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)
