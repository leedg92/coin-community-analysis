#!/bin/bash

# 환경 설정 불러오기
eval "$(grep -o '"[^"]*": [0-9]*' config/default.ts | sed 's/"//g' | sed 's/: /=/')"

# Docker 컨테이너 시작
echo "Starting Docker containers..."
docker-compose up -d
docker-compose -f docker/docker-compose.yml up -d

# Java 백엔드 시작 (8080 포트)
echo "Starting Java backend on port $javaBackend..."
cd backend-java
./mvnw spring-boot:run &
cd ..

# Node.js 백엔드 시작 (3001 포트)
echo "Starting Node.js backend on port $nodeBackend..."
cd backend-node
npm run dev &
cd ..

# BFF 시작 (3000 포트)
echo "Starting BFF on port $bff..."
cd bff
npm run dev &
cd ..

# 프론트엔드 시작 (3002 포트)
echo "Starting Frontend on port $frontend..."
cd frontend
npm run dev &
cd ..

echo "All services are starting..." 