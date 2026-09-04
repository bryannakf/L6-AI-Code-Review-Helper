SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "java"
]

MAX_CODE_LENGTH = 10000


def validate_code(code, language):

    if not code:
        return False, "Code is required"

    if not language:
        return False, "Language is required"

    if len(code) > MAX_CODE_LENGTH:
        return False, "Code exceeds the maximum allowed length of 10,000 characters"

    supported_languages = ["python", "javascript", "js"]

    if language.lower() not in supported_languages:
        return False, f"Unsupported language: {language}"

    return True, None