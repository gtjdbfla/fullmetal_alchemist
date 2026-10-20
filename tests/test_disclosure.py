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
        self.assertEqual(len(self.public["manuscripts"]), 22)
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
        chapter_eighteen = self.public["manuscripts"][-4]
        self.assertEqual(chapter_eighteen["episode"], "제18화")
        self.assertEqual(chapter_eighteen["title"], "소위 그라우스")
        self.assertTrue(chapter_eighteen["text"].startswith("아침 일곱 시."))
        self.assertNotIn("간략 분석", chapter_eighteen["text"])
        self.assertIn("바르크 소위", chapter_eighteen["text"])
        self.assertNotIn("바크 소위", chapter_eighteen["text"])
        chapter_nineteen = self.public["manuscripts"][-3]
        self.assertEqual(chapter_nineteen["episode"], "제19화")
        self.assertEqual(chapter_nineteen["title"], "황제의 백성")
        self.assertTrue(chapter_nineteen["text"].startswith("싱 서북부."))
        self.assertIn("나는 졌지만 바이족은 사라지지 않았으니까.", chapter_nineteen["text"])
        self.assertNotIn("간략 분석", chapter_nineteen["text"])
        chapter_twenty = self.public["manuscripts"][-2]
        self.assertEqual(chapter_twenty["episode"], "제20화")
        self.assertEqual(chapter_twenty["title"], "황제가 되는 법")
        self.assertTrue(chapter_twenty["text"].startswith("다음 날 아침."))
        self.assertIn("다음 황제는?", chapter_twenty["text"])
        self.assertNotIn("간략 분석", chapter_twenty["text"])
        chapter_twenty_one = self.public["manuscripts"][-1]
        self.assertEqual(chapter_twenty_one["episode"], "제21화")
        self.assertEqual(chapter_twenty_one["title"], "두 번째 린")
        self.assertTrue(chapter_twenty_one["text"].startswith("란시 북문을 나서자 길의 모양부터 달라졌다."))
        self.assertIn("해야 할 일이 바뀐 것뿐입니다.", chapter_twenty_one["text"])
        self.assertNotIn("간략 분석", chapter_twenty_one["text"])
        self.assertNotIn("history", self.public)

    def test_public_character_cards_are_spoiler_limited(self):
        self.assertEqual(len(self.public["publicCharacters"]), 28)
        edward = next(item for item in self.public["publicCharacters"] if item["name"] == "에드워드 엘릭")
        self.assertIn("연금술을 잃은", edward["summary"])
        self.assertIn("relationship", edward)
        hasim = next(item for item in self.public["publicCharacters"] if item["name"] == "하심")
        self.assertEqual(hasim["group"], "이슈발 · 재건과 옛 기록")
        self.assertIn("옛길", hasim["relationship"])
        bark = next(item for item in self.public["publicCharacters"] if item["name"] == "바르크")
        self.assertIn("젊은 장교", bark["summary"])
        luhan = next(item for item in self.public["publicCharacters"] if item["name"] == "루한 바이")
        self.assertIn("바이족", luhan["affiliation"])
        self.assertNotIn("결말", " ".join(item["summary"] for item in self.public["publicCharacters"]))

    def test_author_keeps_legacy_versions_outside_public_data(self):
        self.assertEqual(self.author["audience"], "author")
        self.assertEqual(len(self.author["history"]), 3)
        self.assertTrue(all(item["text"].strip() for item in self.author["history"]))

    def test_analysis_is_only_available_to_author_data(self):
        self.assertNotIn("analysis", self.public)
        self.assertNotIn("chapterReviews", self.public)
        self.assertNotIn("storyline", self.public)
        self.assertNotIn("storyBible", self.public)
        self.assertNotIn("sourceDocuments", self.public)
        self.assertEqual(set(self.author["analysis"]), {"characters", "causality", "world"})
        reviews = self.author["chapterReviews"]
        self.assertEqual(len(reviews), 21)
        self.assertTrue(all(3 <= len(item["categories"]) <= 4 for item in reviews))
        chapter_seventeen = next(item for item in reviews if item["episode"] == "제17화")
        self.assertEqual(len(chapter_seventeen["categories"]), 4)
        self.assertTrue(all(0 <= item["score"] <= 10 for item in reviews))

    def test_storyline_map_is_only_available_to_author_data(self):
        storyline = self.author["storyline"]
        self.assertEqual(storyline["currentChapter"], 21)
        self.assertEqual(storyline["totalChapters"], 42)
        self.assertEqual(len(storyline["parts"]), 9)
        self.assertGreaterEqual(len(storyline["threads"]), 5)
        bible = self.author["storyBible"]
        self.assertEqual(len(bible["chapters"]), 44)
        self.assertTrue(any(item["name"] == "바르크" for item in bible["characterArcs"]))
        self.assertTrue(any(item["id"] == "BARK-COMPLETION" for item in bible["foreshadowing"]))
        self.assertIn("hiddenArchitecture", bible)
        self.assertTrue(any(item["id"] == "INFORMATION-INTERPRETATION" for item in bible["foreshadowing"]))

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
            self.assertGreater(len(path.read_text(encoding="utf-8")), 200)
        self.assertEqual({item["version"] for item in self.config["sourceDocuments"]}, {"6.1"})
        self.assertIn("story_bible/01_STORYLINE_CH18_42.md", {item["file"] for item in self.config["sourceDocuments"]})

    def test_private_storyline_is_not_copied_to_public_site(self):
        self.assertFalse((ROOT / "site/STORYLINE_MASTER_v2.0.md").exists())
        self.assertFalse((ROOT / "author-site/STORYLINE_MASTER_v2.0.md").exists())


if __name__ == "__main__":
    unittest.main()
