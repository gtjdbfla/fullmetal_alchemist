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

    def test_public_has_only_current_manuscripts_and_no_history(self):
        self.assertEqual(self.public["audience"], "reader")
        self.assertEqual(len(self.public["manuscripts"]), 19)
        prologue, chapter_one, chapter_two = self.public["manuscripts"][:3]
        self.assertEqual(prologue["episode"], "프롤로그")
        self.assertTrue(prologue["text"].startswith("“거기 아니야.”"))
        self.assertNotIn("# 프롤로그", prologue["text"])
        self.assertEqual(chapter_one["episode"], "제1화")
        self.assertTrue(chapter_one["text"].startswith("편지는 생각보다 길었다."))
        self.assertIn("스카 씨의 형 말이야.", chapter_one["text"])
        self.assertNotIn("# 제1화", chapter_one["text"])
        self.assertEqual(chapter_two["episode"], "제2화")
        self.assertTrue(chapter_two["text"].startswith("이슈발은 에드가 기억하던 곳과 달랐다."))
        self.assertIn("이슈발라란 무엇인가.", chapter_two["text"])
        self.assertNotIn("# 제2화", chapter_two["text"])
        chapter_eighteen = self.public["manuscripts"][-1]
        self.assertEqual(chapter_eighteen["episode"], "제18화")
        self.assertEqual(chapter_eighteen["title"], "소위 그라우스")
        self.assertTrue(chapter_eighteen["text"].startswith("아침 일곱 시."))
        self.assertNotIn("간략 분석", chapter_eighteen["text"])
        self.assertNotIn("history", self.public)

    def test_public_character_cards_are_spoiler_limited(self):
        self.assertGreaterEqual(len(self.public["publicCharacters"]), 10)
        edward = next(item for item in self.public["publicCharacters"] if item["name"] == "에드워드 엘릭")
        self.assertIn("연금술을 잃은", edward["summary"])
        self.assertNotIn("결말", " ".join(item["summary"] for item in self.public["publicCharacters"]))

    def test_author_keeps_legacy_versions_outside_public_data(self):
        self.assertEqual(self.author["audience"], "author")
        self.assertEqual(len(self.author["history"]), 3)
        self.assertTrue(all(item["text"].strip() for item in self.author["history"]))

    def test_analysis_is_only_available_to_author_data(self):
        self.assertNotIn("analysis", self.public)
        self.assertNotIn("chapterReviews", self.public)
        self.assertEqual(set(self.author["analysis"]), {"characters", "causality", "world"})
        self.assertEqual(self.author["chapterReviews"], [])

    def test_mystery_board_separates_ed_hypothesis_from_story_state(self):
        mysteries = self.author["analysis"]["causality"]["mysteries"]
        self.assertEqual(len(mysteries), 5)
        self.assertTrue(all({"question", "hypothesis", "counterEvidence", "actualState"} <= set(item) for item in mysteries))
        ishvala = next(item for item in mysteries if item["question"] == "이슈발라는 무엇인가")
        self.assertIn("진리", ishvala["hypothesis"])
        self.assertIn("동일하지 않다", ishvala["actualState"])

    def test_source_documents_are_saved_privately(self):
        for item in self.config["sourceDocuments"]:
            path = ROOT / item["file"]
            self.assertTrue(path.exists(), item["file"])
            self.assertGreater(len(path.read_text(encoding="utf-8")), 10000)
        self.assertEqual({item["version"] for item in self.config["sourceDocuments"]}, {"3.0", "4.0"})

    def test_private_storyline_is_not_copied_to_public_site(self):
        self.assertFalse((ROOT / "site/STORYLINE_MASTER_v2.0.md").exists())
        self.assertFalse((ROOT / "author-site/STORYLINE_MASTER_v2.0.md").exists())


if __name__ == "__main__":
    unittest.main()
