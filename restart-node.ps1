# Node.js 프로세스 종료
Get-Process | Where-Object { $_.ProcessName -like "*node*" } | Stop-Process -Force

# Node.js 백엔드 재시작
Write-Host "Restarting Node.js backend..." -ForegroundColor Green
Set-Location backend-node
Start-Process powershell -ArgumentList "npm run dev"
Set-Location ..

Write-Host "Node.js backend is restarting..." -ForegroundColor Green 