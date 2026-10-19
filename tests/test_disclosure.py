import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DashboardDisclosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.public = json.loads((ROOT / "site/data/project.json").read_text(encoding="utf-8"))
        cls.author = json.loads((ROOT / "author-site/data/project.json").read_text(encoding="utf-8"))
        cls.config = json.loads((ROOT / "private/dashboard-config.json").read_text(encoding="utf-8"))

    def test_public_has_only_current_manuscript_and_no_history(self):
        self.assertEqual(self.public["audience"], "reader")
        self.assertEqual(len(self.public["manuscripts"]), 1)
        manuscript = self.public["manuscripts"][0]
        self.assertEqual(manuscript["episode"], "프롤로그")
        self.assertTrue(manuscript["text"].startswith("“거기 아니야.”"))
        self.assertNotIn("# 프롤로그", manuscript["text"])
        self.assertNotIn("history", self.public)

    def test_author_keeps_legacy_versions_outside_public_data(self):
        self.assertEqual(self.author["audience"], "author")
        self.assertEqual(len(self.author["history"]), 3)
        self.assertTrue(all(item["text"].strip() for item in self.author["history"]))

    def test_dashboard_has_only_requested_analysis_groups(self):
        self.assertEqual(set(self.public["analysis"]), {"characters", "causality", "world"})

    def test_source_documents_are_saved_privately(self):
        for item in self.config["sourceDocuments"]:
            path = ROOT / item["file"]
            self.assertTrue(path.exists(), item["file"])
            self.assertGreater(len(path.read_text(encoding="utf-8")), 10000)

    def test_private_storyline_is_not_copied_to_public_site(self):
        self.assertFalse((ROOT / "site/STORYLINE_MASTER_v2.0.md").exists())
        self.assertFalse((ROOT / "author-site/STORYLINE_MASTER_v2.0.md").exists())


if __name__ == "__main__":
    unittest.main()
