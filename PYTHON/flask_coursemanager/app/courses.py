from flask import Blueprint, request, jsonify

courses_bp = Blueprint("courses", __name__)

courses = [
    {
        "id": 1,
        "name": "Python Programming",
        "code": "CS101",
        "credits": 4,
        "department": "Computer Science"
    },
    {
        "id": 2,
        "name": "Database Systems",
        "code": "CS102",
        "credits": 3,
        "department": "Computer Science"
    }
]


@courses_bp.route("/")
def home():
    return jsonify({
        "message": "Course Management API Running"
    })


@courses_bp.route("/api/courses", methods=["GET"])
def get_courses():

    return jsonify(courses)


@courses_bp.route("/api/courses/<int:id>", methods=["GET"])
def get_course(id):

    for course in courses:

        if course["id"] == id:
            return jsonify(course)

    return jsonify({"error": "Course not found"}), 404


@courses_bp.route("/api/courses", methods=["POST"])
def create_course():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    required_fields = [
        "name",
        "code",
        "credits",
        "department"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify(
                {"error": f"{field} is required"}
            ), 400

    new_course = {
        "id": len(courses) + 1,
        "name": data["name"],
        "code": data["code"],
        "credits": data["credits"],
        "department": data["department"]
    }

    courses.append(new_course)

    return jsonify(new_course), 201