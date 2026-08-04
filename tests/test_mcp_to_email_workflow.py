import json
import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / "examples" / "n8n-fictional-mcp-to-email-workflow.json"
PROOF_PATH = ROOT / "docs" / "mcp-to-email-fixed-scope-proof.md"
README_PATH = ROOT / "README.md"


class FictionalMcpToEmailWorkflowTest(unittest.TestCase):
    def test_workflow_file_exists(self):
        self.assertTrue(
            WORKFLOW_PATH.is_file(),
            "The importable fictional MCP-to-email workflow must exist",
        )

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_workflow_is_valid_inactive_json_without_credentials(self):
        raw = WORKFLOW_PATH.read_text(encoding="utf-8")
        workflow = json.loads(raw)
        self.assertFalse(workflow["active"])
        self.assertGreaterEqual(len(workflow["nodes"]), 8)
        for node in workflow["nodes"]:
            self.assertNotIn("credentials", node)

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_node_names_ids_and_connections_are_consistent(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        names = [node["name"] for node in workflow["nodes"]]
        ids = [node["id"] for node in workflow["nodes"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(workflow["connections"]).issubset(set(names)))
        for outputs in workflow["connections"].values():
            for branch in outputs["main"]:
                for connection in branch:
                    self.assertIn(connection["node"], names)

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_required_mcp_to_email_stages_are_present(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        names = {node["name"] for node in workflow["nodes"]}
        self.assertTrue(
            {
                "Fictional MCP Responses",
                "Normalize and Validate",
                "Deduplicate by Request ID",
                "Ready for Email?",
                "Human Review Queue",
                "Prepare Email Report",
                "Email Destination (Disabled)",
            }.issubset(names)
        )

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_fixture_covers_normal_duplicate_and_missing_summary_cases(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        fixture_code = next(
            node["parameters"]["jsCode"]
            for node in workflow["nodes"]
            if node["name"] == "Fictional MCP Responses"
        )
        self.assertEqual(fixture_code.count("request_id:"), 3)
        self.assertGreaterEqual(fixture_code.count("demo-request-001"), 2)
        self.assertIn("demo-request-002", fixture_code)
        self.assertIn("summary: ''", fixture_code)

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_duplicate_and_invalid_records_route_to_review(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        dedupe_code = next(
            node["parameters"]["jsCode"]
            for node in workflow["nodes"]
            if node["name"] == "Deduplicate by Request ID"
        )
        review_code = next(
            node["parameters"]["jsCode"]
            for node in workflow["nodes"]
            if node["name"] == "Human Review Queue"
        )
        self.assertIn("duplicate_request_id", dedupe_code)
        self.assertIn("needs_review: true", dedupe_code)
        self.assertIn("send_email: false", review_code)

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_email_destination_is_disabled_and_bounded(self):
        workflow = json.loads(WORKFLOW_PATH.read_text(encoding="utf-8"))
        email_node = next(
            node
            for node in workflow["nodes"]
            if node["name"] == "Email Destination (Disabled)"
        )
        self.assertTrue(email_node["disabled"])
        self.assertEqual(email_node["type"], "n8n-nodes-base.emailSend")
        self.assertTrue(email_node["retryOnFail"])
        self.assertEqual(email_node["maxTries"], 3)
        self.assertEqual(email_node["waitBetweenTries"], 1000)

    @unittest.skipUnless(WORKFLOW_PATH.exists(), "workflow not implemented yet")
    def test_public_fixture_contains_no_live_urls_emails_or_secret_markers(self):
        raw = WORKFLOW_PATH.read_text(encoding="utf-8")
        lowered = raw.lower()
        for marker in (
            "api_key",
            "apikey",
            "access_token",
            "authorization: bearer",
            "password",
            "client_secret",
            "smtp.",
        ):
            self.assertNotIn(marker, lowered)
        self.assertNotIn("n8n-nodes-base.httpRequest", raw)

        urls = re.findall(r"https?://[^\s'\"\\]+", raw)
        self.assertTrue(urls)
        self.assertTrue(all("example.invalid" in url for url in urls))

        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", raw)
        self.assertTrue(emails)
        self.assertTrue(all(email.endswith("@example.invalid") for email in emails))

    def test_readme_links_workflow_and_proof_document(self):
        readme = README_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "examples/n8n-fictional-mcp-to-email-workflow.json",
            readme,
        )
        self.assertIn("docs/mcp-to-email-fixed-scope-proof.md", readme)

    def test_proof_document_defines_observable_paths_and_boundaries(self):
        self.assertTrue(PROOF_PATH.is_file())
        proof = PROOF_PATH.read_text(encoding="utf-8")
        for required_text in (
            "Sanitized input contract",
            "Expected normal path",
            "Expected human review path",
            "Email Destination (Disabled)",
            "Production boundary",
            "USD 139",
            "48 hours",
        ):
            self.assertIn(required_text, proof)


if __name__ == "__main__":
    unittest.main()
