from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


REQUIRED_FIELDS = ("source", "url", "title", "published_at", "author")
SUPPORTED_SOURCES = {"fictional_tiktok", "fictional_instagram", "fictional_youtube"}
TRACKING_QUERY_KEYS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"}
TOPIC_RULES = {
    "food": {"food", "cuisine", "recipe", "noodle", "tea"},
    "technology": {"technology", "robot", "battery", "ev", "ai", "drone"},
    "travel": {"travel", "landscape", "mountain", "village", "city"},
    "culture": {"culture", "heritage", "festival", "craft", "opera"},
}


@dataclass(frozen=True)
class Signal:
    signal_id: str
    source: str
    url: str
    title: str
    description: str
    published_at: str
    author: str
    views: int
    likes: int
    comments: int
    shares: int
    topic: str
    confidence: float
    score: float
    review_status: str
    review_reason: str


def normalize_text(value: object) -> str:
    text = str(value or "").strip().lower()
    return re.sub(r"\s+", " ", text)


def normalize_url(value: object) -> str:
    raw = str(value or "").strip()
    parts = urlsplit(raw)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("url must be an absolute http or https URL")
    query = [
        (key, item)
        for key, item in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_QUERY_KEYS
    ]
    path = parts.path.rstrip("/") or "/"
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, urlencode(query), ""))


def parse_timestamp(value: object) -> datetime:
    raw = str(value or "").strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(raw)
    if parsed.tzinfo is None:
        raise ValueError("published_at must include a timezone")
    return parsed.astimezone(UTC)


def parse_metric(record: dict[str, object], key: str) -> int:
    value = int(record.get(key, 0) or 0)
    if value < 0:
        raise ValueError(f"{key} cannot be negative")
    return value


def classify(title: str, description: str) -> tuple[str, float]:
    tokens = set(re.findall(r"[a-z0-9]+", f"{title} {description}".lower()))
    matches = {
        topic: len(tokens.intersection(keywords))
        for topic, keywords in TOPIC_RULES.items()
    }
    topic, count = max(matches.items(), key=lambda item: (item[1], item[0]))
    if count == 0:
        return "other", 0.0
    return topic, min(1.0, 0.55 + 0.15 * (count - 1))


def identity_key(url: str, title: str) -> str:
    basis = f"{normalize_url(url)}\n{normalize_text(title)}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def signal_score(
    *,
    views: int,
    likes: int,
    comments: int,
    shares: int,
    published_at: datetime,
    as_of: datetime,
    source_count: int,
) -> float:
    age_hours = max(0.0, (as_of - published_at).total_seconds() / 3600)
    engagement = views + likes * 4 + comments * 8 + shares * 12
    recency = math.exp(-age_hours / 72)
    cross_source_bonus = 1 + 0.15 * max(0, source_count - 1)
    return round(math.log1p(engagement) * recency * cross_source_bonus, 4)


def validate_record(record: dict[str, object]) -> None:
    for field in REQUIRED_FIELDS:
        if not str(record.get(field, "")).strip():
            raise ValueError(f"missing required field: {field}")
    if record["source"] not in SUPPORTED_SOURCES:
        raise ValueError(f"unsupported fictional source: {record['source']}")


def build_signal(
    record: dict[str, object],
    *,
    as_of: datetime,
    source_count: int,
) -> Signal:
    validate_record(record)
    url = normalize_url(record["url"])
    title = str(record["title"]).strip()
    description = str(record.get("description", "")).strip()
    published_at = parse_timestamp(record["published_at"])
    metrics = {key: parse_metric(record, key) for key in ("views", "likes", "comments", "shares")}
    topic, confidence = classify(title, description)
    review_reason = "" if confidence >= 0.55 else "classification confidence below 0.55"
    return Signal(
        signal_id=identity_key(url, title),
        source=str(record["source"]),
        url=url,
        title=title,
        description=description,
        published_at=published_at.isoformat().replace("+00:00", "Z"),
        author=str(record["author"]).strip(),
        topic=topic,
        confidence=confidence,
        score=signal_score(
            **metrics,
            published_at=published_at,
            as_of=as_of,
            source_count=source_count,
        ),
        review_status="review" if review_reason else "accepted",
        review_reason=review_reason,
        **metrics,
    )


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: Iterable[Signal]) -> None:
    fields = list(Signal.__dataclass_fields__)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def run_pipeline(input_path: Path, output_dir: Path, *, as_of: datetime) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_records: list[dict[str, object]] = []
    errors: list[dict[str, object]] = []
    for line_number, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            if not isinstance(record, dict):
                raise ValueError("record must be a JSON object")
            raw_records.append(record)
        except (json.JSONDecodeError, ValueError) as exc:
            errors.append({"line": line_number, "error": str(exc)})

    url_counts: dict[str, set[str]] = {}
    for record in raw_records:
        try:
            url = normalize_url(record.get("url"))
            url_counts.setdefault(url, set()).add(str(record.get("source", "")))
        except ValueError:
            pass

    best_by_id: dict[str, Signal] = {}
    for index, record in enumerate(raw_records, start=1):
        try:
            url = normalize_url(record.get("url"))
            signal = build_signal(
                record,
                as_of=as_of.astimezone(UTC),
                source_count=len(url_counts.get(url, set())),
            )
            current = best_by_id.get(signal.signal_id)
            if current is None or signal.score > current.score:
                best_by_id[signal.signal_id] = signal
        except (TypeError, ValueError) as exc:
            errors.append({"record": index, "error": str(exc)})

    signals = sorted(best_by_id.values(), key=lambda row: (-row.score, row.signal_id))
    accepted = [row for row in signals if row.review_status == "accepted"]
    review = [row for row in signals if row.review_status == "review"]

    signals_path = output_dir / "signals.csv"
    review_path = output_dir / "review.csv"
    errors_path = output_dir / "errors.jsonl"
    receipt_path = output_dir / "run-receipt.json"
    write_csv(signals_path, accepted)
    write_csv(review_path, review)
    errors_path.write_text(
        "".join(json.dumps(error, ensure_ascii=False, sort_keys=True) + "\n" for error in errors),
        encoding="utf-8",
    )
    receipt = {
        "as_of": as_of.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        "input_records": len(raw_records),
        "unique_records": len(signals),
        "accepted_records": len(accepted),
        "review_records": len(review),
        "error_records": len(errors),
        "fictional_data": True,
        "hashes": {
            "signals.csv": file_hash(signals_path),
            "review.csv": file_hash(review_path),
            "errors.jsonl": file_hash(errors_path),
        },
    }
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt
