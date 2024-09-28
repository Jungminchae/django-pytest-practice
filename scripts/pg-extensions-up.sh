#!/bin/bash

# PostgreSQL 컨테이너 이름
CONTAINER_NAME="postgres-db"

# PostgreSQL 사용자 및 데이터베이스 이름 (필요에 맞게 수정)
POSTGRES_USER="postgres"
DATABASE_NAME="postgres"

# Docker 컨테이너에서 hstore 확장 설치 명령어 실행
docker exec -it "$CONTAINER_NAME" psql -U "$POSTGRES_USER" -d "$DATABASE_NAME" -c "CREATE EXTENSION IF NOT EXISTS hstore;"
docker exec -it "$CONTAINER_NAME" psql -U "$POSTGRES_USER" -d "$DATABASE_NAME" -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;"

# 성공 메시지 출력
if [ $? -eq 0 ]; then
  echo "extensions successfully created in $DATABASE_NAME."
else
  echo "Failed to create extensions."
fi