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

    def test_displayed_manuscripts_stay_within_loose_length_ceiling(self):
        over_limit = [
            (chapter["episode"], chapter["characters"])
            for chapter in self.public["manuscripts"]
            if chapter["characters"] > 9000
        ]
        self.assertEqual(over_limit, [])
        for chapter in self.public["manuscripts"]:
            self.assertEqual(chapter["characters"], len(chapter["text"].replace("==", "").replace("~~", "")))

    def test_public_has_only_current_manuscripts_and_no_history(self):
        self.assertEqual(self.public["audience"], "reader")
        self.assertEqual(len(self.public["manuscripts"]), 44)
        prologue, chapter_one, chapter_two = self.public["manuscripts"][:3]
        self.assertEqual(prologue["episode"], "프롤로그")
        self.assertTrue(prologue["text"].startswith("“거기 아니야.”"))
        self.assertNotIn("# 프롤로그", prologue["text"])
        self.assertEqual(chapter_one["episode"], "제1화")
        self.assertTrue(chapter_one["text"].startswith("여관 주인이 두툼한 봉투를 내밀었다."))
        self.assertIn("스카 씨의 형 말이야.", chapter_one["text"])
        self.assertNotIn("# 제1화", chapter_one["text"])
        self.assertEqual(chapter_two["episode"], "제2화")
        self.assertTrue(chapter_two["text"].startswith("이슈발은 에드가 기억하던 곳과 달랐다."))
        self.assertIn("이슈발라란 무엇인가.", chapter_two["text"])
        self.assertNotIn("# 제2화", chapter_two["text"])
        chapter_eighteen = next(item for item in self.public["manuscripts"] if item["episode"] == "제18화")
        self.assertEqual(chapter_eighteen["episode"], "제18화")
        self.assertEqual(chapter_eighteen["title"], "중위 그라우스")
        self.assertTrue(chapter_eighteen["text"].startswith("아침 일곱 시."))
        self.assertNotIn("간략 분석", chapter_eighteen["text"])
        self.assertIn("바르크 소위", chapter_eighteen["text"])
        self.assertNotIn("바크 소위", chapter_eighteen["text"])
        chapter_nineteen = next(item for item in self.public["manuscripts"] if item["episode"] == "제19화")
        self.assertEqual(chapter_nineteen["episode"], "제19화")
        self.assertEqual(chapter_nineteen["title"], "황제의 백성")
        self.assertTrue(chapter_nineteen["text"].startswith("싱 서북부."))
        self.assertIn("나는 졌지만 바이족은 사라지지 않았으니까.", chapter_nineteen["text"])
        self.assertNotIn("간략 분석", chapter_nineteen["text"])
        chapter_twenty = next(item for item in self.public["manuscripts"] if item["episode"] == "제20화")
        self.assertEqual(chapter_twenty["episode"], "제20화")
        self.assertEqual(chapter_twenty["title"], "황제가 되는 법")
        self.assertTrue(chapter_twenty["text"].startswith("다음 날 아침."))
        self.assertIn("다음 황제는?", chapter_twenty["text"])
        self.assertNotIn("간략 분석", chapter_twenty["text"])
        chapter_twenty_one = next(item for item in self.public["manuscripts"] if item["episode"] == "제21화")
        self.assertEqual(chapter_twenty_one["episode"], "제21화")
        self.assertEqual(chapter_twenty_one["title"], "두 번째 린")
        self.assertTrue(chapter_twenty_one["text"].startswith("란시 북문을 나서자 길의 모양부터 달라졌다."))
        self.assertIn("해야 할 일이 바뀐 것뿐입니다.", chapter_twenty_one["text"])
        self.assertNotIn("간략 분석", chapter_twenty_one["text"])
        chapter_twenty_two = next(item for item in self.public["manuscripts"] if item["episode"] == "제22화")
        self.assertEqual(chapter_twenty_two["episode"], "제22화")
        self.assertEqual(chapter_twenty_two["title"], "길은 양쪽으로 열린다")
        self.assertTrue(chapter_twenty_two["text"].startswith("다음 날 아침"))
        self.assertIn("빼앗은 것도 황제였고.", chapter_twenty_two["text"])
        self.assertNotIn("22화 분석", chapter_twenty_two["text"])
        chapter_twenty_three = next(item for item in self.public["manuscripts"] if item["episode"] == "제23화")
        self.assertEqual(chapter_twenty_three["episode"], "제23화")
        self.assertEqual(chapter_twenty_three["title"], "좋은 재료")
        self.assertTrue(chapter_twenty_three["text"].startswith("크림스톤은 불에 넣어도 쉽게 무너지지 않았다."))
        self.assertIn("길도 거래망도 전부터 있었다.", chapter_twenty_three["text"])
        self.assertNotIn("23화 분석", chapter_twenty_three["text"])
        chapter_twenty_four = next(item for item in self.public["manuscripts"] if item["episode"] == "제24화")
        self.assertEqual(chapter_twenty_four["episode"], "제24화")
        self.assertEqual(chapter_twenty_four["title"], "두 개의 미래")
        self.assertTrue(chapter_twenty_four["text"].startswith("무란허를 다녀온 날 저녁, 린은 다시 란시로 돌아왔다."))
        self.assertIn("그렇게 엿새가 지났다.", chapter_twenty_four["text"])
        self.assertIn("너는 칼 안 가져가?", chapter_twenty_four["text"])
        self.assertNotIn("연성진", chapter_twenty_four["text"])
        self.assertNotIn("24화 분석", chapter_twenty_four["text"])
        self.assertNotIn("history", self.public)

    def test_new_approved_chapters_and_corrected_titles(self):
        expected = {25: "황제를 죽이는 사람", 26: "발자취", 27: "선을 넘는 사람", 28: "불이 없는 전쟁", 29: "총통을 움직이는 법", 30: "바이족의 아들", 31: "세 번의 총성", 32: "다시 시작한 전쟁", 33: "황제가 아닌 사람", 34: "한 사람", 35: "칼을 드는 이유", 36: "마지막 한 발", 37: "전쟁이 끝난 자리", 38: "재판", 39: "황제가 없는 나라", 40: "마지막 총통", 41: "누가 결정하는가", 42: "남은 질문"}
        for number, title in expected.items():
            chapter = next(item for item in self.public["manuscripts"] if item["episode"] == f"제{number}화")
            self.assertEqual(chapter["title"], title)
            self.assertNotIn(f"{number}화 분석", chapter["text"])
        self.assertIn("반 호엔하임", next(item for item in self.public["manuscripts"] if item["episode"] == "제26화")["text"])
        self.assertEqual(self.public["manuscripts"][-1]["episode"], "에필로그")

    def test_revised_karsa_chapters_are_current_manuscripts(self):
        expected = {9: "사막으로", 10: "길을 지운 사람들", 11: "형이 걸었던 길", 12: "흐르는 땅", 13: "서쪽에서 온 사람"}
        for number, title in expected.items():
            chapter = next(item for item in self.public["manuscripts"] if item["episode"] == f"제{number}화")
            self.assertEqual(chapter["title"], title)
            self.assertNotIn(f"제{number}화 검증", chapter["text"])
            self.assertNotIn("하산", chapter["text"])
        chapter_twelve = next(item for item in self.public["manuscripts"] if item["episode"] == "제12화")
        self.assertIn("대가가 없는 게 아니야", chapter_twelve["text"])

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
        self.assertEqual(len(reviews), 43)
        self.assertTrue(all(len(item["categories"]) == 4 for item in reviews))
        self.assertTrue(all({c["name"] for c in item["categories"]} == {"캐릭터", "개연성", "스토리라인", "세계관·복선"} for item in reviews))
        self.assertTrue(all(c["status"] in {"O", "△", "X"} for item in reviews for c in item["categories"]))
        self.assertTrue(all("score" not in item for item in reviews))
        chapter_seventeen = next(item for item in reviews if item["episode"] == "제17화")
        self.assertEqual(len(chapter_seventeen["categories"]), 4)
        self.assertTrue(all(item["length"]["characters"] > 0 for item in reviews))

    def test_storyline_map_is_only_available_to_author_data(self):
        storyline = self.author["storyline"]
        self.assertEqual(storyline["currentChapter"], 42)
        self.assertEqual(storyline["totalChapters"], 42)
        self.assertEqual(len(storyline["parts"]), 9)
        self.assertGreaterEqual(len(storyline["threads"]), 5)
        self.assertEqual(set(storyline["tabs"]), {"chapters", "settings", "foreshadowing"})
        self.assertTrue(any(item["chapter"] == "12화" for item in storyline["settingsMilestones"]))
        bible = self.author["storyBible"]
        self.assertEqual(len(bible["chapters"]), 44)
        self.assertTrue(any(item["name"] == "바르크" for item in bible["characterArcs"]))
        self.assertTrue(any(item["id"] == "BARK-COMPLETION" for item in bible["foreshadowing"]))
        self.assertIn("hiddenArchitecture", bible)
        self.assertTrue(any(item["id"] == "INFORMATION-INTERPRETATION" for item in bible["foreshadowing"]))
        self.assertTrue(any(item["id"] == "KARSA-EXCHANGE" and item["status"] == "PAYOFF" for item in bible["foreshadowing"]))

    def test_world_hard_update_is_explained_in_settings_and_rules(self):
        bible = self.author["storyBible"]
        self.assertEqual(bible["version"], "8.1")
        groups = self.author["storyline"]["tabs"]["settings"]["groups"]
        self.assertEqual([group["label"] for group in groups], ["캐릭터", "기술과 미스터리", "역사·정치·지리", "이슈발라·기록·흐름 문장"])
        cards = {item["title"]: item for group in groups for item in group["items"]}
        self.assertGreaterEqual(len(cards), 18)
        self.assertIn("용맥", cards["싱의 연단술과 용맥"]["description"])
        self.assertIn("하나의 연성진", cards["카이룬의 넓은 흐름 독해"]["description"])
        self.assertIn("옛 안족 영역", cards["세 시대의 동쪽 이동"]["description"])
        self.assertIn("카르사를 우회", cards["남부 교역로의 최종 선택"]["description"])
        self.assertTrue(all(len(item["canon"]) > 30 for item in cards.values()))
        rules = {item["rule"] for item in bible["hardRules"]}
        self.assertIn("흐름의 물리적 경계", rules)
        self.assertIn("카이룬의 기원과 유일성 금지", rules)
        self.assertIn("시대별 이동 경로와 길 선택", rules)

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
        self.assertEqual({item["version"] for item in self.config["sourceDocuments"]}, {"7.0", "7.1", "8.0", "8.1"})
        self.assertIn("story_bible/01_STORYLINE_CH18_42.md", {item["file"] for item in self.config["sourceDocuments"]})
        self.assertIn("story_bible/11_WORLD_HARD_UPDATE.md", {item["file"] for item in self.config["sourceDocuments"]})

    def test_private_storyline_is_not_copied_to_public_site(self):
        self.assertFalse((ROOT / "site/STORYLINE_MASTER_v2.0.md").exists())
        self.assertFalse((ROOT / "author-site/STORYLINE_MASTER_v2.0.md").exists())

    def test_public_characters_have_appearance_and_optional_portrait(self):
        for person in self.public["publicCharacters"]:
            self.assertTrue(person.get("appearance"), person["name"])
            self.assertTrue(person.get("age"), person["name"])
            if person.get("portrait"):
                self.assertTrue((ROOT / "site" / person["portrait"]).exists(), person["name"])
                self.assertTrue((ROOT / "author-site" / person["portrait"]).exists(), person["name"])

    def test_foreshadowing_ledger_matches_the_manuscripts(self):
        import sys
        sys.path.insert(0, str(ROOT / "scripts"))
        import ledger_check
        config = json.loads((ROOT / "private" / "dashboard-config.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger_check.check(config), [])

    def test_note_markers_are_balanced_and_absent_from_txt(self):
        for item in self.public["manuscripts"]:
            for paragraph in item["text"].split("\n\n"):
                self.assertEqual(paragraph.count("==") % 2, 0, (item["episode"], paragraph[:30]))
                self.assertEqual(paragraph.count("~~") % 2, 0, (item["episode"], paragraph[:30]))
        for txt in (ROOT / "publish" / "txt").glob("*.txt"):
            body = txt.read_text(encoding="utf-8")
            self.assertNotIn("==", body, txt.name)
            self.assertNotIn("~~", body, txt.name)


if __name__ == "__main__":
    unittest.main()
