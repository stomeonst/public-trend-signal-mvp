from __future__ import annotations

import csv
import json
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from trend_signal.pipeline import (
    classify,
    identity_key,
    normalize_url,
    run_pipeline,
    signal_score,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "fictional_signals.jsonl"
AS_OF = datetime(2026, 7, 27, tzinfo=UTC)


class PipelineTests(unittest.TestCase):
    def test_tracking_parameters_are_removed(self) -> None:
        self.assertEqual(
            normalize_url("HTTPS://Example.Test/path/?utm_source=x&a=1"),
            "https://example.test/path?a=1",
        )

    def test_identity_is_stable_after_tracking_cleanup(self) -> None:
        first = identity_key("https://example.test/x?utm_campaign=a", "  Same Title ")
        second = identity_key("https://example.test/x", "same   title")
        self.assertEqual(first, second)

    def test_classifier_routes_unknown_topic_to_review(self) -> None:
        self.assertEqual(classify("Morning observations", "quiet notes"), ("other", 0.0))

    def test_score_rewards_fresher_signal(self) -> None:
        common = dict(views=1000, likes=100, comments=10, shares=5, as_of=AS_OF, source_count=1)
        fresh = signal_score(published_at=datetime(2026, 7, 26, tzinfo=UTC), **common)
        old = signal_score(published_at=datetime(2026, 7, 20, tzinfo=UTC), **common)
        self.assertGreater(fresh, old)

    def test_end_to_end_outputs_are_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first = run_pipeline(FIXTURE, Path(first_dir), as_of=AS_OF)
            second = run_pipeline(FIXTURE, Path(second_dir), as_of=AS_OF)
            self.assertEqual(first, second)
            self.assertEqual(first["input_records"], 5)
            self.assertEqual(first["unique_records"], 3)
            self.assertEqual(first["accepted_records"], 2)
            self.assertEqual(first["review_records"], 1)
            self.assertEqual(first["error_records"], 1)

            with (Path(first_dir) / "signals.csv").open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["review_status"], "accepted")

            receipt = json.loads((Path(first_dir) / "run-receipt.json").read_text(encoding="utf-8"))
            self.assertTrue(receipt["fictional_data"])


if __name__ == "__main__":
    unittest.main()
