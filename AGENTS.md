# Story data and disclosure

- 사용자가 확정한 이야기와 원고를 보존한다. 스토리·대사·연구 근거·이동 사건을 임의로 창작하거나 원고를 자동 수정하지 않는다.
- 기준 우선순위: 출처가 확인된 원작 CANON → 사용자 Story Master Plan → 제출 원고 → 초기 구계획. 충돌은 기록하고 사용자에게 알린다. 사용자 확정 창작 설정은 ORIGINAL이며 원작 CANON으로 승격하지 않는다.
- `private/STORY_MASTER_PLAN_v2.md`와 `private/master-data.json`이 활성 작가 기준이다. v1.0은 보존 이력이다. 실제 설정, 현재 인물 가설, 독자 공개 정보, 공개 예정 시점을 별도 필드로 유지한다. 미래에 가질 가설을 현재 인물 지식에 넣지 않는다.
- Political Board의 명시된 요구·예시·미정 양보선을 구분한다. 가칭 적맥석의 정확한 성질·A/B부족 이름·협상 비율을 임의 확정하지 않는다. 미공개 자원·정치 정보는 제목부터 공개 데이터에서 제외한다.
- `site/`는 공개 정적 루트다. 결말과 미공개 설정은 화면 숨김만으로 보호하지 않는다. `private/`와 `author-site/`를 공개 루트에 복사하지 않는다. 작가용 서비스는 tailnet 전용이며 Funnel로 공개하지 않는다.
- 최종 빌드: `python scripts/build_views.py`. `publish_manuscripts.py`만 단독 실행한 결과를 배포하지 않는다.
- 배포 전 `node --test tests/core.test.mjs`, `node --check site/app.js`, `python -m unittest discover -s tests -p test_disclosure.py`를 실행한다. 공개/작가용 화면과 공개 데이터 격리를 확인한다.
- 모든 미래 화수를 임의 고정하지 않는다. 미정 공개 시점은 null과 단계명으로 관리한다. SOLVED는 실제 근거가 필요하다.
