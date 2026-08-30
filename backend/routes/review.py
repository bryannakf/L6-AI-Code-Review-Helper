from flask import Blueprint, request, jsonify
from utils.validation import validate_code

review_bp = Blueprint("review", __name__)


@review_bp.route("/review", methods=["POST"])
def review_code():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No request data provided"
        }), 400

    code = data.get("code")
    language = data.get("language")

    valid, error = validate_code(code, language)

    if not valid:
        return jsonify({
            "error": error
        }), 400

    return jsonify({
        "message": "Code received successfully",
        "language": language
    })