#!/bin/bash

# Next.js 프론트엔드 프로세스 종료
pkill -f "next dev.*frontend"

# 프론트엔드 재시작
echo "Restarting Frontend..."
cd frontend
npm run dev &
cd ..

echo "Frontend is restarting..." 