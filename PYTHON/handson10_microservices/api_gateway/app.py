import os
import requests
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

COURSE_SERVICE_URL = os.environ.get("COURSE_SERVICE_URL", "http://localhost:5001")
STUDENT_SERVICE_URL = os.environ.get("STUDENT_SERVICE_URL", "http://localhost:5002")


@app.route('/')
def home():
    return jsonify({
        "service": "API Gateway",
        "port": 5000,
        "routes": {
            "/api/courses/*": COURSE_SERVICE_URL,
            "/api/departments/*": COURSE_SERVICE_URL,
            "/api/students/*": STUDENT_SERVICE_URL
        }
    })


@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    if path.startswith('courses') or path.startswith('departments'):
        target_service = COURSE_SERVICE_URL
    elif path.startswith('students'):
        target_service = STUDENT_SERVICE_URL
    else:
        return jsonify({"error": "Route not found on API Gateway"}), 404

    target_url = f"{target_service}/api/{path}"

    # Forward headers excluding Host
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            allow_redirects=False
        )

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, response_headers)

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Service Unavailable",
            "message": f"Could not connect to service at {target_service}",
            "details": str(e)
        }), 503


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
