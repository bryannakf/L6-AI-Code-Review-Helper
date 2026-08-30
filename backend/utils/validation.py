SUPPORTED_LANGUAGES = [
    "python",
    "javascript",
    "java"
]

MAX_CODE_LENGTH = 10000


def validate_code(code, language):

    if not code or not code.strip():
        return False, "Code cannot be empty."

    if len(code) > MAX_CODE_LENGTH:
        return False, "Code exceeds the maximum permitted length."

    if language not in SUPPORTED_LANGUAGES:
        return False, f"Unsupported language: {language}"

    return True, None