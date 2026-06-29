from flask import jsonify


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404


    @app.errorhandler(400)
    def bad_request(error):

        return jsonify({
            "status": "error",
            "message": "Bad Request"
        }), 400