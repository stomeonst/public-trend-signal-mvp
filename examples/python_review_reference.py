"""Reference correction for the fictional code-review fixture."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from numbers import Real
from typing import Any


def unique_recent_titles(
    records: Iterable[Mapping[str, Any]],
    minimum_score: Real = 0,
) -> list[str]:
    """Return normalized unique titles whose numeric score meets the threshold."""
    if isinstance(minimum_score, bool) or not isinstance(minimum_score, Real):
        raise TypeError("minimum_score must be a real number")

    seen: set[str] = set()
    output: list[str] = []

    for index, record in enumerate(records):
        raw_title = record.get("title")
        score = record.get("score")
        if not isinstance(raw_title, str):
            raise ValueError(f"record {index} has no string title")
        if isinstance(score, bool) or not isinstance(score, Real):
            raise ValueError(f"record {index} has no numeric score")

        title = " ".join(raw_title.split())
        if not title:
            raise ValueError(f"record {index} has an empty title")

        identity = title.casefold()
        if score >= minimum_score and identity not in seen:
            output.append(title)
            seen.add(identity)

    return output
