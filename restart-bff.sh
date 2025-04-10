#!/bin/bash

# BFF 프로세스 종료
pkill -f "next dev.*bff"

# BFF 재시작
echo "Restarting BFF..."
cd bff
npm run dev &
cd ..

echo "BFF is restarting..." 