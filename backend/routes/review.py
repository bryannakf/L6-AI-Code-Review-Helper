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

    # Start overall timer
    start_time = time.perf_counter()

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

    # 3. Run static analysis
    static_start = time.perf_counter()

    if language.lower() == "python":

        static_results = analyse_python(code)

    elif language.lower() in ["javascript", "js"]:

        static_results = analyse_javascript(code)

    else:

        return jsonify({
            "error": f"Unsupported language: {language}"
        }), 400

    static_end = time.perf_counter()

    static_analysis_time = round(
        static_end - static_start,
        2
    )

    # 4. Run AI analysis
    ai_start = time.perf_counter()

    ai_results = analyse_code(code, language)

    ai_end = time.perf_counter()

    ai_analysis_time = round(
        ai_end - ai_start,
        2
    )

    # Check whether AI analysis succeeded
    ai_available = "error" not in ai_results

    # 5. Calculate score
    score_start = time.perf_counter()

    if ai_available:

        score = calculate_score(
            static_results.get("issues", []),
            ai_results.get("issues", [])
        )

    else:

        # Continue using static-analysis results
        # if the AI service is unavailable.
        score = calculate_score(
            static_results.get("issues", []),
            []
        )

    score_end = time.perf_counter()

    score_calculation_time = round(
        score_end - score_start,
        2
    )

    # Calculate total analysis time
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

        "ai_feedback": {
            "available": ai_available,
            "error": (
                "AI analysis unavailable"
                if not ai_available
                else None
            )
        },

        "score": score,

        "analysis_time": analysis_time,

        "performance": {
            "static_analysis_time": static_analysis_time,
            "ai_analysis_time": ai_analysis_time,
            "score_calculation_time": score_calculation_time
        }
    })