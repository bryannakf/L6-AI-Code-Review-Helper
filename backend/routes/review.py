import time

from flask import Blueprint, request, jsonify

from backend.utils.validation import validate_code
from backend.services.pylint_service import analyse_python
from backend.services.eslint_service import analyse_javascript
from backend.services.csharp_service import analyse_csharp
from backend.services.ai_service import analyse_code
from backend.services.scoring_service import calculate_score
from backend.utils.security import detect_secrets


review_bp = Blueprint("review", __name__)


@review_bp.route("/review", methods=["POST"])
def review_code():

    try:
        # Start overall timer
        start_time = time.perf_counter()

        # 1. Get request
        data = request.get_json(silent=True) or {}

        if not isinstance(data, dict):
            return jsonify({
                "error": "No request data provided"
            }), 400

        code = data.get("code")
        language = data.get("language")

        # Indicates that the user has confirmed that a
        # detected secret-like pattern is not sensitive information.
        secret_confirmed = data.get("secret_confirmed", False)

        # 2. Validate request
        valid, error = validate_code(code, language)

        if not valid:
            return jsonify({
                "error": error
            }), 400

        # 3. Check for potential secrets
        secret_findings = detect_secrets(code)

        # If a potential secret is detected, ask the user to confirm
        # that it is not sensitive information before continuing.
        if secret_findings and not secret_confirmed:
            return jsonify({
                "security": {
                    "secrets_detected": True,
                    "confirmation_required": True,
                    "issues": secret_findings
                }
            }), 200

        # 4. Run static analysis
        static_start = time.perf_counter()

        if language.lower() == "python":
            static_results = analyse_python(code)

        elif language.lower() in ["javascript", "js"]:
            static_results = analyse_javascript(code)

        elif language.lower() == "csharp":
            static_results = analyse_csharp(code)

        else:
            return jsonify({
                "error": f"Unsupported language: {language}"
            }), 400

        static_end = time.perf_counter()

        static_analysis_time = round(
            static_end - static_start,
            2
        )

        # Support different result formats returned by
        # the language-specific analysis services.
        static_issues = static_results.get(
            "findings",
            static_results.get("issues", [])
        )

        static_analysis = {
            "tool": static_results.get("tool", "Unknown"),
            "issues": static_issues,
            "error": static_results.get("error")
        }

        # 5. Run AI analysis
        ai_start = time.perf_counter()

        ai_results = analyse_code(
            code,
            language
        )

        ai_end = time.perf_counter()

        ai_analysis_time = round(
            ai_end - ai_start,
            2
        )

        ai_available = (
            isinstance(ai_results, dict)
            and "error" not in ai_results
        )

        # 6. Calculate score
        score_start = time.perf_counter()

        if ai_available:
            score = calculate_score(
                static_issues,
                ai_results.get("issues", [])
            )
        else:
            score = calculate_score(
                static_issues,
                []
            )

        score_end = time.perf_counter()

        score_calculation_time = round(
            score_end - score_start,
            2
        )

        # 7. Calculate total analysis time
        end_time = time.perf_counter()

        analysis_time = round(
            end_time - start_time,
            2
        )

        # 8. Return results
        return jsonify({
            "language": language,

            "static_analysis": static_analysis,

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

    except Exception as exc:
        return jsonify({
            "error": "Internal server error while reviewing code.",
            "details": str(exc)
        }), 500