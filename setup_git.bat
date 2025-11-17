@echo off
REM Git Repository Initialization Script
REM This script initializes the Git repository for Hospital Management System

cd /d "c:\Users\Atharva Madhavapeddi\Desktop\IITM Project\hospital-management-system"

echo.
echo ============================================================
echo   Hospital Management System - Git Repository Setup
echo ============================================================
echo.

echo [1/5] Initializing Git repository...
git init
if errorlevel 1 goto error

echo.
echo [2/5] Configuring Git user...
git config user.name "Atharva Madhavapeddi"
git config user.email "23f2001926@ds.study.iitm.ac.in"
if errorlevel 1 goto error

echo.
echo [3/5] Adding all files...
git add .
if errorlevel 1 goto error

echo.
echo [4/5] Creating initial commit...
git commit -m "Initial commit: Hospital Management System with multi-role authentication, 3 dashboards, and complete healthcare features"
if errorlevel 1 goto error

echo.
echo [5/5] Displaying commit history...
git log --oneline -n 5

echo.
echo ============================================================
echo   Git Repository Setup Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Create a repository on your Git Tracker platform
echo 2. Add remote: git remote add origin [YOUR_GIT_URL]
echo 3. Push code: git push -u origin main
echo.

goto end

:error
echo.
echo ERROR: Git command failed!
echo Please ensure Git is properly installed and in your PATH
echo.

:end
pause
