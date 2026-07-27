"""Intentionally flawed review fixture using fictional records."""


def unique_recent_titles(records, minimum_score=0):
    """Return titles for records at or above the score threshold."""
    seen = set()
    output = []
    for record in records:
        title = record["title"].strip()
        if record["score"] >= minimum_score and title not in seen:
            output.append(title)
        seen.add(title)
    return output
