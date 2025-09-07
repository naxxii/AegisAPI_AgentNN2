# AegisAPI AgentNN - React Dashboard Setup
Write-Host "🚀 AegisAPI AgentNN - React Dashboard Setup" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host ""

Write-Host "📦 Checking for npm..." -ForegroundColor Yellow

# Check if npm is available
try {
    $npmVersion = npm --version 2>$null
    Write-Host "✅ npm found: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ npm not found. Installing Node.js..." -ForegroundColor Red
    Write-Host ""

    # Try to install Node.js using Chocolatey
    try {
        choco install nodejs --yes 2>$null
        Write-Host "✅ Node.js installed via Chocolatey" -ForegroundColor Green
    } catch {
        Write-Host "❌ Chocolatey not available or installation failed." -ForegroundColor Red
        Write-Host ""
        Write-Host "🔧 Please install Node.js manually:" -ForegroundColor Yellow
        Write-Host "   1. Go to: https://nodejs.org/" -ForegroundColor White
        Write-Host "   2. Download the LTS version" -ForegroundColor White
        Write-Host "   3. Install it" -ForegroundColor White
        Write-Host "   4. Restart this script" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 Alternative: Use the HTML dashboard at http://localhost:8080" -ForegroundColor Cyan
        Read-Host "Press Enter to exit"
        exit 1
    }

    # Refresh PATH and check npm again
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    try {
        $npmVersion = npm --version 2>$null
        Write-Host "✅ npm verified: $npmVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ npm still not available after installation" -ForegroundColor Red
        Write-Host "💡 Alternative: Use the HTML dashboard at http://localhost:8080" -ForegroundColor Cyan
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "📱 Setting up React dashboard..." -ForegroundColor Yellow

# Navigate to dashboard directory
Set-Location dashboard

# Install dependencies
npm install

Write-Host ""
Write-Host "🎉 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Starting React dashboard..." -ForegroundColor Yellow

# Start the React development server
npm start

Write-Host ""
Write-Host "💡 React dashboard will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "💡 HTML dashboard is available at: http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"
