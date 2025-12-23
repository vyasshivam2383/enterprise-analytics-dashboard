@echo off
REM Enterprise Analytics Dashboard - Quick Deploy Script
REM This script prepares your app for deployment

echo.
echo ====================================================================
echo  ENTERPRISE ANALYTICS DASHBOARD - DEPLOYMENT SETUP
echo ====================================================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo Step 1: Initializing Git repository...
git init
if errorlevel 1 (
    echo WARNING: Git repository already exists
)

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: Enterprise Analytics Dashboard - Production Ready"
if errorlevel 1 (
    echo WARNING: No changes to commit
)

echo.
echo ====================================================================
echo.
echo NEXT STEPS:
echo.
echo 1. Create a NEW repository on GitHub:
echo    - Go to: https://github.com/new
echo    - Name it: enterprise_analytics_dashboard
echo    - Description: Production-ready analytics dashboard with AI Q&A
echo    - Click "Create repository"
echo.
echo 2. Copy-paste the following commands in your terminal:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/enterprise_analytics_dashboard
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Go to Streamlit Cloud:
echo    - Visit: https://share.streamlit.io
echo    - Click "Create app"
echo    - Select YOUR_USERNAME/enterprise_analytics_dashboard
echo    - Select branch: main, file: app.py
echo    - Click "Deploy"
echo.
echo Your app will be LIVE in 1-2 minutes at:
echo https://enterprise-analytics-dashboard-YOUR_USERNAME.streamlit.app
echo.
echo ====================================================================
echo.
pause
