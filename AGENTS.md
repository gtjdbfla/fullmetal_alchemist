# Story data and dashboard rules

- 사용자가 확정한 이야기와 원고를 임의로 창작하거나 수정하지 않는다.
- 활성 정답지는 `private/STORYLINE_MASTER_v3.0.md`, 검증 규칙은 `private/STORY_DASHBOARD_SPEC_v3.0.md`다.
- 원작 CANON, 원작과 양립 가능한 창작 설정, 추측, 인물의 틀린 가설을 분리한다.
- 공개 메뉴는 글 읽기와 글 분석 두 개만 유지한다. 분석 하위 분류는 캐릭터·개연성·세계관이다.
- 글 읽기는 목차에서 선택한 프롤로그 또는 회차 하나만 보여준다. 원고 하단에는 이전화·다음화·맨 위로(목차) 이동을 둔다.
- 현재 원고만 `site/data/project.json`에 넣는다. 이전 버전과 폐기 원고는 공개 데이터에 절대 포함하지 않는다.
- 과거 버전은 관리자 화면과 Git 이력에서만 확인한다. 관리자용 `author-site`는 tailnet 전용이며 Funnel로 공개하지 않는다.
- 스토리라인과 검증 규칙 원문은 `private/`에 둔다. 공개 또는 관리자 정적 루트로 복사하지 않는다.
- 최종 빌드는 `python scripts/build_views.py`로 만든다.
- 배포 전 `node --test tests/core.test.mjs`, `node --check site/app.js`, `python -m unittest discover -s tests -p test_disclosure.py`를 실행한다.
