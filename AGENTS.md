# Story data and dashboard rules

- 사용자가 확정한 이야기와 원고를 임의로 창작하거나 수정하지 않는다.
- 활성 정답지는 세계관 HARD UPDATE `story_bible/11_WORLD_HARD_UPDATE.md`, `story_bible/12_CH25_32_APPROVED_UPDATE.md`, `story_bible/09_LATEST_INTEGRATED_UPDATE.md`, Ch9~13 개정 범위의 `story_bible/10_CH09_13_REVISION.md` 및 최신 승인 원고, `private/dashboard-config.json`의 `storyBible` 구조화 데이터다. `private/STORYLINE_MASTER_v5.0.md`와 이전 문서는 참조 보관본이다.
- 원작 CANON, 원작과 양립 가능한 창작 설정, 추측, 인물의 틀린 가설을 분리한다.
- 공개 메뉴는 글 읽기와 등장인물 두 개만 유지한다. 글 분석과 Story Bible은 `/east/admin/` 관리자 모드에서만 연다.
- Story Bible 변경은 인과 체인·인물 아크·복선·지식 상태·하드 룰에 미칠 영향을 함께 기록한다.
- 승인 원고와 Story Bible이 충돌하면 어느 한쪽을 자동 수정하지 않고 사용자에게 충돌을 보고한다.
- 등장인물 카드는 소속별로 묶고, 각 카드에 현재 이야기에서의 간략한 연관성을 표시한다.
- 관리자 분석은 회차별로 캐릭터·개연성·스토리라인·세계관/복선을 O·△·X로 검토하고 짧은 이유·다음 원고 점검 항목을 남긴다. 공백 포함 본문 글자 수와 4,800~5,000자 기준을 전체 회차에 표시한다.
- 글 읽기는 목차에서 선택한 프롤로그 또는 회차 하나만 보여준다. 원고 하단에는 이전화·다음화·맨 위로(목차) 이동을 둔다.
- 현재 원고만 `site/data/project.json`에 넣는다. Story Bible·검토 데이터·이전 버전·폐기 원고는 공개 데이터에 절대 포함하지 않는다.
- 과거 버전은 관리자 화면과 Git 이력에서만 확인한다. 관리자용 `author-site`는 `/east/admin/` 경로로 제공한다.
- Story Bible과 검증 규칙 원문은 `story_bible/` 및 `private/`에 둔다. 공개 또는 관리자 정적 루트로 문서를 복사하지 않는다.
- 최종 빌드는 `python scripts/build_views.py`로 만든다.
- 배포 전 `node --test tests/core.test.mjs`, `node --check site/app.js`, `python -m unittest discover -s tests -p test_disclosure.py`를 실행한다.
