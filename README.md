# 통합 작가 대시보드

사용자 요청(2026-10-24)으로 독자 모드를 제거했다. 기본 `/east/`와 기존 `/east/admin/`에서 글 읽기·등장인물·글 분석·스토리라인을 모두 제공한다. 등장인물에 기존 Story Bible의 인물 아크·지식 상태를 함께 표시한다. 두 주소는 같은 데이터이며 모드 전환 링크는 없다.

아래 문서의 공개/관리자 구분과 작가 데이터 제외 설명은 과거 구성 기록이다. 현재 빌드는 두 정적 루트에 같은 작가 데이터를 생성한다. 원고·설정 내용은 바꾸지 않았다.

# 강철의 연금술사 — 동쪽으로

망상연구소의 소설 프로젝트 대시보드다.

- 공개 화면: https://yulmserver.tail261e6c.ts.net:10000/east/
- 관리자 화면: https://yulmserver.tail261e6c.ts.net:10000/east/admin/
- GitHub: https://github.com/gtjdbfla/fullmetal_alchemist

## 화면 구조

공개 메뉴는 글 읽기와 등장인물 두 개만 유지한다.

1. 글 읽기
   - 목차에서 프롤로그와 각 회차를 하나씩 선택해 읽는다.
   - 원고 하단에서 이전화·다음화·맨 위로(목차) 이동을 제공한다.
2. 등장인물
   - 현재 공개된 회차를 기준으로 한 짧은 소개만 제공한다.
   - 후반 전개와 결말은 공개하지 않는다.
글 분석은 관리자 모드에서만 연다. 회차별로 캐릭터, 개연성·스토리라인, 세계관, 복선·다음 질문을 각각 10점 만점으로 검토하며, 원고 근거와 다음 회차 점검 항목을 남긴다. 공개 화면의 등장인물은 소속별로 나누고 인물 간 연결을 함께 적는다.

현재 원고는 `manuscripts/current/`에서 불러온다. 이전 원고와 분석 데이터는 공개 JSON에서 제거했고 관리자 화면에서만 확인할 수 있다. 이후 원고 수정본도 현재본만 공개하고 과거 버전은 관리자 데이터에만 둔다.

## 기준 문서

- `story_bible/`: 18~42화·에필로그 기준의 활성 Story Bible. 핵심 규칙, 스토리라인, 인물, 세계관, 인과 체인, 복선, 지식 상태, 집필·검증 규칙으로 분리한다.
- `private/dashboard-config.json`의 `storyBible`: 관리자 대시보드가 읽는 구조화된 기준 데이터
- `private/STORY_DASHBOARD_SPEC_v3.0.md`: 기존 검증 규칙 보관본
- `private/STORYLINE_MASTER_v5.0.md`: 이전 활성 스토리라인 보관본

Story Bible 문서와 검증 규칙은 공개 정적 루트로 복사하지 않는다.

## 빌드와 실행

```powershell
python scripts/build_views.py
python scripts/serve.py
```

작가 화면은 다음과 같이 연다.

```powershell
python scripts/serve.py --author
```

## 검증

```powershell
node --test tests/core.test.mjs
node --check site/app.js
python -m unittest discover -s tests -p test_disclosure.py
```
