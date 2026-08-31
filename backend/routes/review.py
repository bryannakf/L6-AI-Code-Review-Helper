import time
from flask import Blueprint, request, jsonify

from utils.validation import validate_code
from services.pylint_service import analyse_python
from services.eslint_service import analyse_javascript
from services.ai_service import analyse_code
from services.scoring_service import calculate_score


review_bp = Blueprint("review", __name__)


@review_bp.route("/review", methods=["POST"])
def review_code():

    # 1. Get request
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No request data provided"
        }), 400

    code = data.get("code")
    language = data.get("language")

    # 2. Validate request
    valid, error = validate_code(code, language)

    if not valid:
        return jsonify({
            "error": error
        }), 400
    #3 start timer
    import time

    start_time = time.perf_counter()

    # 3. Run static analysis
    if language.lower() == "python":

        static_results = analyse_python(code)

    elif language.lower() in ["javascript", "js"]:

        static_results = analyse_javascript(code)

    else:

        return jsonify({
            "error": f"Unsupported language: {language}"
        }), 400

    # Extract static-analysis issues for scoring
    static_issues = static_results.get("issues", [])

    # 4. Run AI analysis
    ai_results = analyse_code(code, language)

    # Extract AI issues for scoring
    ai_issues = ai_results.get("issues", [])

    # 5. Calculate score
    score = calculate_score(
        static_issues,
        ai_issues
    )
    # stop timer
    end_time = time.perf_counter()
    analysis_time = round(
        end_time - start_time,
        2
    )
    # 6. Return results
    return jsonify({
        "language": language,
        "static_analysis": static_results,
        "ai_analysis": ai_results,
        "score": score,
        "analysis_time": analysis_time
    })