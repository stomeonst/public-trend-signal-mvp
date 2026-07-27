from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublicDocumentationTests(unittest.TestCase):
    def test_readme_links_to_existing_public_samples(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        sample_paths = [
            "docs/python-code-review-sample.md",
            "docs/simplified-chinese-ai-evaluation-sample.md",
            "docs/english-to-simplified-chinese-translation-evaluation-sample.md",
        ]

        for relative_path in sample_paths:
            with self.subTest(relative_path=relative_path):
                self.assertIn(relative_path, readme)
                self.assertTrue((ROOT / relative_path).is_file())

    def test_translation_sample_preserves_public_evidence_boundary(self):
        sample = (
            ROOT
            / "docs"
            / "english-to-simplified-chinese-translation-evaluation-sample.md"
        ).read_text(encoding="utf-8")

        self.assertIn("has not already been refunded", sample)
        self.assertIn("尚未退款", sample)
        self.assertIn("Critical", sample)
        self.assertIn("no customer text", sample.lower())
        self.assertIn("private benchmark", sample.lower())


if __name__ == "__main__":
    unittest.main()
