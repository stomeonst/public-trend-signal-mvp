import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / "examples" / "n8n-public-trend-signal-workflow.json"


class PublicN8nWorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = json.loads(cls.raw)

    def test_workflow_is_inactive_and_credential_free(self):
        self.assertFalse(self.workflow["active"])
        for node in self.workflow["nodes"]:
            self.assertNotIn("credentials", node)

    def test_node_names_and_ids_are_unique(self):
        names = [node["name"] for node in self.workflow["nodes"]]
        ids = [node["id"] for node in self.workflow["nodes"]]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(len(ids), len(set(ids)))

    def test_connections_only_target_existing_nodes(self):
        names = {node["name"] for node in self.workflow["nodes"]}
        self.assertTrue(set(self.workflow["connections"]).issubset(names))
        for outputs in self.workflow["connections"].values():
            for branch in outputs["main"]:
                for connection in branch:
                    self.assertIn(connection["node"], names)

    def test_workflow_has_required_evidence_stages(self):
        names = {node["name"] for node in self.workflow["nodes"]}
        self.assertTrue(
            {
                "Fictional Input",
                "Normalize and Deduplicate",
                "Score with Evidence Gate",
                "Needs Human Review?",
                "Human Review Queue",
                "Authorized Table Output",
            }.issubset(names)
        )

    def test_no_secret_markers_or_live_api_nodes(self):
        lowered = self.raw.lower()
        for marker in (
            "api_key",
            "apikey",
            "access_token",
            "authorization: bearer",
            "password",
            "client_secret",
        ):
            self.assertNotIn(marker, lowered)
        node_types = {node["type"] for node in self.workflow["nodes"]}
        self.assertNotIn("n8n-nodes-base.httpRequest", node_types)

    def test_fixture_uses_reserved_example_domain(self):
        code = next(
            node["parameters"]["jsCode"]
            for node in self.workflow["nodes"]
            if node["name"] == "Fictional Input"
        )
        self.assertIn("example.invalid", code)
        self.assertNotIn("tiktok.com", code.lower())
        self.assertNotIn("instagram.com", code.lower())
        self.assertNotIn("youtube.com", code.lower())


if __name__ == "__main__":
    unittest.main()
