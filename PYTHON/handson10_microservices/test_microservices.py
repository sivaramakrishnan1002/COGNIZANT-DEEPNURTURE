import time
import subprocess
import requests
import sys
import unittest

COURSE_SERVICE_URL = "http://localhost:5001"
STUDENT_SERVICE_URL = "http://localhost:5002"
GATEWAY_URL = "http://localhost:5000"

class TestMicroservices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start course_service, student_service, and api_gateway processes
        cls.course_proc = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd="course_service"
        )
        cls.student_proc = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd="student_service"
        )
        cls.gateway_proc = subprocess.Popen(
            [sys.executable, "app.py"],
            cwd="api_gateway"
        )

        # Give processes a moment to boot
        time.sleep(3)

    @classmethod
    def tearDownClass(cls):
        for proc in [cls.course_proc, cls.student_proc, cls.gateway_proc]:
            try:
                proc.terminate()
                proc.wait(timeout=2)
            except Exception:
                proc.kill()

    def test_01_services_running_independently(self):
        r_course = requests.get(f"{COURSE_SERVICE_URL}/")
        self.assertEqual(r_course.status_code, 200)
        self.assertEqual(r_course.json().get("port"), 5001)

        r_student = requests.get(f"{STUDENT_SERVICE_URL}/")
        self.assertEqual(r_student.status_code, 200)
        self.assertEqual(r_student.json().get("port"), 5002)

        r_gateway = requests.get(f"{GATEWAY_URL}/")
        self.assertEqual(r_gateway.status_code, 200)
        self.assertEqual(r_gateway.json().get("port"), 5000)

    def test_02_course_service_crud(self):
        # Create course
        payload = {"name": "Python Microservices", "code": "CS101", "credits": 4}
        r = requests.post(f"{COURSE_SERVICE_URL}/api/courses", json=payload)
        self.assertIn(r.status_code, [201, 400])  # 400 if already created from previous run

        # Get courses
        r = requests.get(f"{COURSE_SERVICE_URL}/api/courses")
        self.assertEqual(r.status_code, 200)
        courses = r.json()
        self.assertTrue(len(courses) > 0)
        self.assertTrue(any(c["code"] == "CS101" for c in courses))

    def test_03_student_service_crud(self):
        # Create student
        payload = {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com"}
        r = requests.post(f"{STUDENT_SERVICE_URL}/api/students", json=payload)
        self.assertIn(r.status_code, [201, 400])

        # Get students
        r = requests.get(f"{STUDENT_SERVICE_URL}/api/students")
        self.assertEqual(r.status_code, 200)
        students = r.json()
        self.assertTrue(len(students) > 0)

    def test_04_gateway_routing_and_enrollment_flow(self):
        # Gateway routing to get courses
        r_courses = requests.get(f"{GATEWAY_URL}/api/courses")
        self.assertEqual(r_courses.status_code, 200)
        courses = r_courses.json()
        course_id = courses[0]["id"]

        # Gateway routing to get students
        r_students = requests.get(f"{GATEWAY_URL}/api/students")
        self.assertEqual(r_students.status_code, 200)
        students = r_students.json()
        student_id = students[0]["id"]

        # Test enrollment flow through Gateway: Gateway -> Student Service -> Course Service
        enroll_payload = {"course_id": course_id}
        r_enroll = requests.post(f"{GATEWAY_URL}/api/students/{student_id}/enroll", json=enroll_payload)
        self.assertIn(r_enroll.status_code, [200, 201])
        data = r_enroll.json()
        self.assertIn("enrollment", data)
        self.assertEqual(data["enrollment"]["student_id"], student_id)
        self.assertEqual(data["enrollment"]["course_id"], course_id)

    def test_05_course_service_unavailable(self):
        # Terminate course service process
        self.course_proc.terminate()
        self.course_proc.wait(timeout=2)
        time.sleep(1)

        # Attempt to enroll student when course service is down -> expected 503
        r_enroll = requests.post(f"{GATEWAY_URL}/api/students/1/enroll", json={"course_id": 1})
        self.assertEqual(r_enroll.status_code, 503)
        self.assertIn("Course Service Unavailable", r_enroll.text)

if __name__ == '__main__':
    unittest.main()
