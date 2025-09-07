@echo off
echo 🚀 AegisAPI AgentNN - React Dashboard Setup
echo ===========================================
echo.

echo 📦 Installing npm (Node.js package manager)...
echo.

REM Try to install Node.js/npm using Chocolatey (if available)
choco install nodejs --yes 2>nul

REM Check if npm is now available
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm installation failed or npm not found.
    echo.
    echo 🔧 Please install Node.js manually:
    echo    1. Go to: https://nodejs.org/
    echo    2. Download the LTS version
    echo    3. Install it
    echo    4. Restart this script
    echo.
    echo 💡 Alternative: Use the HTML dashboard at http://localhost:8080
    pause
    exit /b 1
)

echo ✅ npm installed successfully!
echo.

echo 📱 Setting up React dashboard...
cd dashboard
npm install

echo.
echo 🎉 Setup complete!
echo.
echo 🌐 Starting React dashboard...
npm start

echo.
echo 💡 React dashboard will be available at: http://localhost:3000
echo 💡 HTML dashboard is available at: http://localhost:8080
echo.
pause
