# 환경 설정 불러오기
$config = Get-Content -Raw -Path "config/default.ts" | ForEach-Object { 
    if ($_ -match '"(frontend|bff|nodeBackend|javaBackend)": (\d+)') {
        Set-Variable -Name $matches[1] -Value $matches[2]
    }
}

# Docker 컨테이너 시작
Write-Host "Starting Docker containers..." -ForegroundColor Green
docker-compose -f docker/docker-compose.yml up -d

# Java 백엔드는 IDE에서 실행해주세요 (8080 포트)
Write-Host "Please run Java backend from IDE on port 8080..." -ForegroundColor Yellow
# Set-Location backend-java
# Start-Process powershell -ArgumentList ".\gradlew.bat bootRun"
# Set-Location ..

# Node.js 백엔드 시작 (3001 포트)
Write-Host "Starting Node.js backend on port $nodeBackend..." -ForegroundColor Green
Set-Location backend-node
Start-Process powershell -ArgumentList "npm run dev"
Set-Location ..

# BFF 시작 (3000 포트)
Write-Host "Starting BFF on port $bff..." -ForegroundColor Green
Set-Location bff
Start-Process powershell -ArgumentList "npm run dev"
Set-Location ..

# 프론트엔드 시작 (3002 포트)
Write-Host "Starting Frontend on port $frontend..." -ForegroundColor Green
Set-Location frontend
Start-Process powershell -ArgumentList "npm run dev"
Set-Location ..

Write-Host "All services are starting..." -ForegroundColor Green 