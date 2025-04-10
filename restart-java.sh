#!/bin/bash

# Java 프로세스 종료
pkill -f "spring-boot:run"

# Java 백엔드 재시작
echo "Restarting Java backend..."
cd backend-java
./mvnw spring-boot:run &
cd ..

echo "Java backend is restarting..." 