# Story data and dashboard rules

- 사용자가 확정한 이야기와 원고를 임의로 창작하거나 수정하지 않는다.
- 활성 정답지는 세계관 HARD UPDATE `story_bible/11_WORLD_HARD_UPDATE.md`, `story_bible/12_CH25_32_APPROVED_UPDATE.md`(Ch33 포함), `story_bible/09_LATEST_INTEGRATED_UPDATE.md`, Ch9~13 개정 범위의 `story_bible/10_CH09_13_REVISION.md` 및 최신 승인 원고, `private/dashboard-config.json`의 `storyBible` 구조화 데이터다. `private/STORYLINE_MASTER_v5.0.md`와 이전 문서는 참조 보관본이다.
- 원작 CANON, 원작과 양립 가능한 창작 설정, 추측, 인물의 틀린 가설을 분리한다.
- 공개 메뉴는 글 읽기와 등장인물 두 개만 유지한다. 글 분석과 Story Bible은 `/east/admin/` 관리자 모드에서만 연다.
- Story Bible 변경은 인과 체인·인물 아크·복선·지식 상태·하드 룰에 미칠 영향을 함께 기록한다.
- 승인 원고와 Story Bible이 충돌하면 어느 한쪽을 자동 수정하지 않고 사용자에게 충돌을 보고한다.
- 등장인물 카드는 소속별로 묶고, 각 카드에 현재 이야기에서의 간략한 연관성을 표시한다.
- 관리자 분석은 회차별로 캐릭터·개연성·스토리라인·세계관/복선을 O·△·X로 검토하고 짧은 이유·다음 원고 점검 항목을 남긴다. 공백 포함 본문 글자 수와 5,000~7,000자 기준을 전체 회차에 표시한다.
- 글 읽기는 목차에서 선택한 프롤로그 또는 회차 하나만 보여준다. 원고 하단에는 이전화·다음화·맨 위로(목차) 이동을 둔다.
- 현재 원고만 `site/data/project.json`에 넣는다. Story Bible·검토 데이터·이전 버전·폐기 원고는 공개 데이터에 절대 포함하지 않는다.
- 과거 버전은 관리자 화면과 Git 이력에서만 확인한다. 관리자용 `author-site`는 `/east/admin/` 경로로 제공한다.
- Story Bible과 검증 규칙 원문은 `story_bible/` 및 `private/`에 둔다. 공개 또는 관리자 정적 루트로 문서를 복사하지 않는다.
- 최종 빌드는 `python scripts/build_views.py`로 만든다.
- 배포 전 `node --test tests/core.test.mjs`, `node --check site/app.js`, `python -m unittest discover -s tests -p test_disclosure.py`를 실행한다.
- 새 원고가 들어오면 `private/dashboard-config.json`의 `storyBible.chapters[].review`에 회차별 검토(개연성·스토리라인·세계관/설정의 O·△·X와 이유, 반영한 수정, 다음 점검)를 쓴다. 관리자 모드 스토리라인의 회차별 카드에 표시된다. 검토한 회차에만 쓰고 읽지 않은 회차는 비워 둔다.
- 새 원고가 설정을 바꾸면 스토리라인의 설정 카드(`storyline.tabs.settings.groups`), 하드 룰, 인물 아크, 지식 상태, 복선 추적, `continuityConflicts`를 원고 기준으로 더 구체적이고 정확하게 고친다. 원고를 고치기 전에 작가에게 확인한다.
- 회차별 연재용 txt는 `python scripts/build_views.py`가 `publish/txt/`에 함께 만든다(제목 첫 줄, 장면 구분은 `* * *`). 이 폴더는 로컬·GitHub·홈서버에 보관한다.
- 이슈발라의 정체는 미스터리로 남기고, 아메스트리스 연금술과 진리의 문 설정은 `story_bible/03_WORLD_MYSTERY.md` 마지막 절을 따른다.

## 복선 장부 규칙

- 복선을 심거나 회수할 때는 `private/dashboard-config.json`의 foreshadowing 항목에 `verify`(화 번호와 원고에 실제로 있는 낱말)를 함께 적는다. `python scripts/ledger_check.py` 가 통과해야 한다.
- 회수하지 않기로 한 것은 상태 `UNRESOLVED_BY_DESIGN`, 본편에서 완성하지 않고 열어 두기로 한 것은 `OPEN_BY_DESIGN`으로 적고 payoff에 의도를 쓴다.
