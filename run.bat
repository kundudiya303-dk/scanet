@echo off
REM ==============================================================================
REM scanet — Single Command One-Click Launcher (Windows)
REM Cloned? Just run: run.bat
REM ==============================================================================
title scanet — Cybersecurity Reconnaissance Platform
cls

echo =============================================================
echo   ____                               _   
echo  / ___|  ___ __ _ _ __   ___| |_ 
echo  \___ \ / __/ _` | '_ \ / _ \ __|
echo   ___) | (_| (_| | | | |  __/ |_ 
echo  |____/ \___\__,_|_| |_|\___|\__|
echo  -------------------------------------------------------------
echo   Lightweight Web-Orchestrated Cybersecurity Platform
echo   Multi-Tool Recon - OS Fingerprinting - AI Security Advisor
echo =============================================================
echo.

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] Error: Python not found in PATH. Please install Python 3.10+.
    pause
    exit /b 1
)

python run.py
pause
