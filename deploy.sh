#!/bin/sh
# 서버에서 크론으로 돈다 (10분마다). GitHub main의 변경을 받아 필요한 만큼만 반영한다.
#   */10 * * * * /home/yulimseo/fullmetal_alchemist/deploy.sh >> /home/yulimseo/fullmetal_alchemist/logs/deploy.log 2>&1
#
# 이 폴더(~/fullmetal_alchemist)는 배포 전용이다 — 개발은 ~/dev/fullmetal_alchemist에서 하고 push한다.
# 여기서 커밋하지 않은 수정은 아래 reset --hard로 사라진다.
#
# site/ · author-site/ 는 Caddy 컨테이너가 디렉터리 볼륨으로 물고 있어 파일이 바뀌면 즉시 서빙된다.
# author-site/ 는 git에 없는 산출물이라 scripts/build_views.py 로 다시 만든다(site/ 를 복사, 제자리 덮어쓰기라 마운트가 유지된다).
# Caddyfile · docker-compose.yml 은 바인드 마운트라 git reset 이 inode 를 바꾸면 컨테이너가 옛 내용을 본다 → 바뀌었을 때만 재생성한다.

set -e
cd "$(dirname "$0")"
mkdir -p logs

exec 9>logs/.lock
flock -n 9 || exit 0

LOG=logs/deploy.log
if [ -f "$LOG" ] && [ "$(wc -l < "$LOG")" -gt 4000 ]; then
    tail -n 2000 "$LOG" > "$LOG.keep" && cat "$LOG.keep" > "$LOG"
    rm -f "$LOG.keep"
fi

BEFORE=$(git rev-parse HEAD)
if ! timeout 60 git fetch -q origin main; then
    echo "$(date '+%F %T') [fail] git fetch 실패"
    exit 1
fi
git reset -q --hard origin/main
AFTER=$(git rev-parse HEAD)

if [ "$BEFORE" = "$AFTER" ] && [ -d author-site ]; then
    exit 0
fi

CHANGED=$(git diff --name-only "$BEFORE" "$AFTER" 2>/dev/null || echo all)
echo "$(date '+%F %T') $BEFORE -> $AFTER"

python3 scripts/build_views.py
case "$CHANGED" in
    *Caddyfile*|*docker-compose.yml*|all)
        docker compose up -d --force-recreate ;;
    *)
        docker compose up -d ;;
esac

for c in east-project east-author; do
    s=$(docker inspect -f '{{.State.Status}}' "$c" 2>/dev/null || echo missing)
    [ "$s" = "running" ] || echo "$(date '+%F %T') [warn] $c 상태: $s"
done
echo "$(date '+%F %T') 배포 완료"
