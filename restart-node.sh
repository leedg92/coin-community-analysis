#!/bin/bash

# Node.js 프로세스 종료
pkill -f "ts-node-dev"

# Node.js 백엔드 재시작
echo "Restarting Node.js backend..."
cd backend-node
npm run dev &
cd ..

echo "Node.js backend is restarting..." 