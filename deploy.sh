#!/bin/sh
# 수동 배포 — 이 폴더의 현재 파일 그대로 반영한다. GitHub는 이력 보관용(매일 자동 커밋·push) — 이 스크립트는 git을 건드리지 않는다.
#   사용: cd ~/fullmetal_alchemist && ./deploy.sh
# site/ · author-site/ 는 Caddy 컨테이너가 디렉터리 볼륨으로 물고 있어 파일이 바뀌면 즉시 서빙된다.
# author-site/ 는 git 에 없는 산출물이라 scripts/build_views.py 로 다시 만든다(제자리 덮어쓰기라 마운트가 유지된다).
set -e
cd "$(dirname "$0")"
mkdir -p logs
echo "$(date '+%F %T') 배포 시작"
python3 scripts/build_views.py
# Caddyfile·compose 는 바인드 마운트라 편집기가 inode 를 바꾸면 컨테이너가 옛 내용을 본다 → 바뀐 경우에만 재생성
SUM=$(cat Caddyfile docker-compose.yml $(ls Author.Caddyfile 2>/dev/null) | md5sum | cut -d' ' -f1)
if [ "$SUM" != "$(cat logs/.deploy_sum 2>/dev/null)" ]; then
    docker compose up -d --force-recreate
    echo "$SUM" > logs/.deploy_sum
else
    docker compose up -d
fi
sleep 5
docker compose ps --format '{{.Name}}  {{.Status}}'
echo "$(date '+%F %T') 배포 완료"
