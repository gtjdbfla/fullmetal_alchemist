# 강철의 연금술사 — 동쪽으로

망상연구소의 소설 프로젝트 대시보드다.

- 공개 화면: https://yulmserver.tail261e6c.ts.net:10000/east/
- 관리자 화면: https://yulmserver.tail261e6c.ts.net:8444/ (Tailscale 전용)
- GitHub: https://github.com/gtjdbfla/fullmetal_alchemist

## 화면 구조

공개 메뉴는 두 개만 유지한다.

1. 글 읽기
   - 프롤로그부터 최신 회차까지 한 화면에서 연속으로 읽는다.
   - 현재 새 스토리라인의 프롤로그가 등록되어 있다.
2. 글 분석
   - 캐릭터
   - 개연성
   - 세계관

현재 원고는 `manuscripts/current/`에서 불러온다. 이전 원고는 공개 데이터에서 제거했고 저장소와 관리자 화면의 이전 원고 보관함에서만 확인할 수 있다. 이후 원고 수정본도 현재본만 공개하고 과거 버전은 관리자 데이터에만 둔다.

## 기준 문서

- `private/STORYLINE_MASTER_v2.0.md`: 작품에서 실제로 일어나는 사건과 최종 방향
- `private/STORY_DASHBOARD_SPEC_v2.0.md`: 원작·캐릭터·인과·정보 흐름·복선을 검사하는 규칙
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
