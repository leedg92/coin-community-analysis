# Next.js 프론트엔드 프로세스 종료
Get-Process | Where-Object { $_.ProcessName -eq "node" -and $_.CommandLine -like "*next dev*" } | Stop-Process -Force

# 프론트엔드 재시작
Write-Host "Restarting Frontend..." -ForegroundColor Green
Set-Location frontend
Start-Process powershell -ArgumentList "npm run dev"
Set-Location ..

Write-Host "Frontend is restarting..." -ForegroundColor Green 