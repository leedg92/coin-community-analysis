# Java 프로세스 종료
Get-Process | Where-Object { $_.ProcessName -like "*java*" } | Stop-Process -Force

# Java 백엔드 재시작
Write-Host "Restarting Java backend..." -ForegroundColor Green
Set-Location backend-java
Start-Process powershell -ArgumentList ".\mvnw spring-boot:run"
Set-Location ..

Write-Host "Java backend is restarting..." -ForegroundColor Green 