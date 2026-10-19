# 강철의 연금술사 — 동쪽으로

망상연구소의 소설 프로젝트 대시보드다.

- 공개 화면: https://yulmserver.tail261e6c.ts.net:10000/east/
- 관리자 화면: https://yulmserver.tail261e6c.ts.net:8444/ (Tailscale 전용)
- GitHub: https://github.com/gtjdbfla/fullmetal_alchemist

## 화면 구조

공개 메뉴는 글 읽기와 등장인물 두 개만 유지한다.

1. 글 읽기
   - 목차에서 프롤로그와 각 회차를 하나씩 선택해 읽는다.
   - 원고 하단에서 이전화·다음화·맨 위로(목차) 이동을 제공한다.
2. 등장인물
   - 현재 공개된 회차를 기준으로 한 짧은 소개만 제공한다.
   - 후반 전개와 결말은 공개하지 않는다.
글 분석은 관리자 모드에서만 연다. 회차별로 캐릭터, 개연성·스토리라인, 세계관, 복선·다음 질문을 각각 10점 만점으로 검토하며, 원고 근거와 다음 회차 점검 항목을 남긴다.

현재 원고는 `manuscripts/current/`에서 불러온다. 이전 원고와 분석 데이터는 공개 JSON에서 제거했고 관리자 화면에서만 확인할 수 있다. 이후 원고 수정본도 현재본만 공개하고 과거 버전은 관리자 데이터에만 둔다.

## 기준 문서

- `private/STORYLINE_MASTER_v4.0.md`: 1~18화 구성과 등장인물, 이후 전개 방향을 반영한 활성 스토리라인
- `private/STORY_DASHBOARD_SPEC_v3.0.md`: 원작·캐릭터·인과·정보 흐름·복선·가설/실제 상태 분리를 검사하는 활성 규칙
- `private/dashboard-config.json`: 두 화면에 필요한 최소 데이터

스토리라인 문서와 검증 규칙은 공개 정적 루트로 복사하지 않는다.

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
