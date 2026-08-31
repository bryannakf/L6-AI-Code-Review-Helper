def calculate_score(static_results, ai_results):

    readability = 100
    maintainability = 100
    style = 100
    bugs = 100

    for issue in static_results:

        issue_type = issue.get("type")

        if issue_type == "error":
            bugs -= 15

        elif issue_type == "warning":
            style -= 5

        elif issue_type == "convention":
            readability -= 3

    for issue in ai_results:

        severity = issue.get("severity")

        if severity == "critical":
            bugs -= 20

        elif severity == "high":
            bugs -= 15

        elif severity == "medium":
            maintainability -= 10

        elif severity == "low":
            readability -= 5

    readability = max(0, readability)
    maintainability = max(0, maintainability)
    style = max(0, style)
    bugs = max(0, bugs)

    overall = (
        readability +
        maintainability +
        style +
        bugs
    ) / 4

    return {
        "overall": round(overall),
        "readability": readability,
        "maintainability": maintainability,
        "style": style,
        "bugs": bugs
    }