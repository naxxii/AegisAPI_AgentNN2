# AegisAPI_AgentNN.ps1
# One-click demo: Plan → Generate → Run → Heal → Re-generate → Re-run → Report

Write-Host "=== Agentic API Test Automation Demo ===" -ForegroundColor Cyan

# Activate venv
.\.venv\Scripts\Activate.ps1

# Kill any old uvicorn
Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*\.venv\*" -and $_.StartInfo.Arguments -like "*uvicorn*" } | Stop-Process -Force

# Start mock server in background
Start-Process powershell -ArgumentList "cd $PWD; .\.venv\Scripts\Activate.ps1; python -m uvicorn mocks.server:app --port 4010"

Start-Sleep -Seconds 3

Write-Host "`n[1] Planning endpoints..." -ForegroundColor Yellow
py -m aegisapi.cli plan --spec .\examples\openapi_v1.yaml --base-url http://localhost:4010

Write-Host "`n[2] Generating tests..." -ForegroundColor Yellow
py -m aegisapi.cli gen --spec .\examples\openapi_v1.yaml --out .\tests_generated

Write-Host "`n[3] Running tests (expected to fail initially)..." -ForegroundColor Yellow
py -m aegisapi.cli run --tests .\tests_generated --spec .\examples\openapi_v1.yaml --base-url http://localhost:4010

Write-Host "`n[4] Reporting results..." -ForegroundColor Yellow
py -m aegisapi.cli report

# Drift simulation
Write-Host "`n[5] Simulating API drift and healing..." -ForegroundColor Yellow
py -m aegisapi.cli heal --old-spec .\examples\openapi_v1.yaml --new-spec .\examples\openapi_v2_drift.yaml --apply

Write-Host "`n[6] Re-generating tests for drifted spec..." -ForegroundColor Yellow
py -m aegisapi.cli gen --spec .\examples\openapi_v2_drift.yaml --out .\tests_generated

Write-Host "`n[7] Re-running tests (with healing applied)..." -ForegroundColor Yellow
py -m aegisapi.cli run --tests .\tests_generated --spec .\examples\openapi_v2_drift.yaml --base-url http://localhost:4010

Write-Host "`n[8] Final report..." -ForegroundColor Yellow
py -m aegisapi.cli report
explorer .\reports\index.html

Write-Host "`n=== Demo Complete! Opened dashboard ===" -ForegroundColor Green
