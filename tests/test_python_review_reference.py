import unittest

from examples.python_review_reference import unique_recent_titles


class PythonReviewReferenceTests(unittest.TestCase):
    def test_low_score_duplicate_does_not_hide_later_eligible_record(self):
        records = [
            {"title": "Same signal", "score": 1},
            {"title": "Same signal", "score": 10},
        ]
        self.assertEqual(unique_recent_titles(records, minimum_score=5), ["Same signal"])

    def test_identity_is_casefolded_and_whitespace_normalized(self):
        records = [
            {"title": "  AI   Workflow ", "score": 9},
            {"title": "ai workflow", "score": 10},
        ]
        self.assertEqual(unique_recent_titles(records, minimum_score=5), ["AI Workflow"])

    def test_rejected_record_does_not_reserve_identity(self):
        records = [
            {"title": "Review Queue", "score": 2},
            {"title": " review   queue ", "score": 8},
        ]
        self.assertEqual(unique_recent_titles(records, minimum_score=5), ["review queue"])

    def test_invalid_title_has_stable_record_index(self):
        with self.assertRaisesRegex(ValueError, "record 1 has no string title"):
            unique_recent_titles(
                [
                    {"title": "Valid", "score": 8},
                    {"title": None, "score": 9},
                ]
            )

    def test_boolean_score_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "record 0 has no numeric score"):
            unique_recent_titles([{"title": "Signal", "score": True}])

    def test_invalid_threshold_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "minimum_score must be a real number"):
            unique_recent_titles([], minimum_score="5")


if __name__ == "__main__":
    unittest.main()
