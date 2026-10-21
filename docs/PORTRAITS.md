# 등장인물 사진 넣는 법

등장인물 페이지의 사진 칸은 기본적으로 **빈칸**이다. 사진은 직접 구한 이미지 파일(저작권·사용 허락은 작가 책임)을 아래 규칙으로 넣으면 자동으로 붙는다.

1. 파일을 `site/portraits/` 에 `<슬러그>.jpg` (또는 `.jpeg` `.png` `.webp`) 로 저장한다. 정면 사진, 가로:세로 약 4:5를 권장한다.
2. `python scripts/build_views.py` 를 실행하면 `site/data/project.json` 에 `portrait` 경로가 붙고 페이지에 나타난다. 파일이 없는 인물은 계속 빈칸이다.
3. 서버 반영은 평소 배포 절차(번들 → 서버 merge → build)와 같다. 사진 파일도 커밋해야 한다.

| 인물 | 슬러그 |
|---|---|
| 에드워드 엘릭 | `edward` |
| 알폰스 엘릭 | `alphonse` |
| 스카 | `scar` |
| 스카의 형 | `scar-brother` |
| 마일즈 | `miles` |
| 아딘 | `adin` |
| 자히르 | `zahir` |
| 하심 | `hashim` |
| 로이 머스탱 | `mustang` |
| 리자 호크아이 | `hawkeye` |
| 에리히 브란트 | `brandt` |
| 그라우스 | `graus` |
| 바르크 | `bark` |
| 린 야오 | `lin` |
| 메이 창 | `mei` |
| 란팡 | `lanfan` |
| 리엔 | `lien` |
| 푸룽 | `purong` |
| 샤오린 | `xiaolin` |
| 천루오 | `tianluo` |
| 루한 바이 | `luhan` |
| 젠하 바이 | `jenha` |
| 웨이 바이 | `wei` |
| 카이룬 | `kairun` |
| 나디르 | `nadir` |
| 사하라 | `sahara` |
| 다우드 | `daud` |
| 마지드 | `majid` |
